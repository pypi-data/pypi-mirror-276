from fsspec.asyn import AsyncFileSystem
from hscitorchutil.processlocal import ProcessLocal
import yaml
import multiprocessing_utils
import asyncio
from concurrent import futures
import datetime
import functools
import mmap
import os
import time
from typing import Any, Awaitable, Callable, Iterable, Tuple, Coroutine
import fsspec
import fsspec.implementations.local
import fsspec.asyn
from fsspec.callbacks import TqdmCallback
from fsspec.implementations.cached import SimpleCacheFileSystem
from fsspec.implementations.cache_mapper import AbstractCacheMapper
from fsspec.caching import Fetcher, MMapCache, register_cache, caches
import fsspec.implementations.local

# The below patches LocalFileSystem to have the removed mv_file method that current AsyncLocalFileSystem version needs


class PatchedLocalFileSystem(fsspec.implementations.local.LocalFileSystem):
    def mv_file(self, src: str, dst: str, **kwargs) -> None:
        self.mv(src, dst, **kwargs)


fsspec.implementations.local.LocalFileSystem = PatchedLocalFileSystem

from morefs.asyn_local import AsyncLocalFileSystem  # noqa


# without this, fsspec hangs in a multiprocessing fork context when it has been already used in the parent process
os.register_at_fork(
    after_in_child=fsspec.asyn.reset_lock,
)

# Async Maps (start, end) to bytes
AFetcher = Callable[[int, int], Awaitable[bytes]]


class PathCacheMapper(AbstractCacheMapper):
    """Cache mapper that uses a hash of the remote URL."""

    def __call__(self, path: str) -> str:
        return '_@_'.join(path.split("/"))


class SharedMMapCache(MMapCache):

    _lock = multiprocessing_utils.SharedLock()
    name = "smmap"

    def __init__(self, blocksize: int, fetcher: Fetcher, size: int, location: str, index_location: str, afetcher: AFetcher | None = None, parallel_timeout=30) -> None:
        self.index_location = index_location
        self.parallel_timeout = parallel_timeout
        self.afetcher = afetcher
        with self._lock:
            super().__init__(blocksize, fetcher, size, location, None)
            self._index = self._makeindex()

    def _makeindex(self) -> mmap.mmap | bytearray:
        if self.size == 0:
            return bytearray()
        if not os.path.exists(self.index_location):
            fd = open(self.index_location, "wb+")
            fd.seek(self.size // self.blocksize)
            fd.write(b'\x00')
            fd.flush()
        else:
            fd = open(self.index_location, "rb+")
        return mmap.mmap(fd.fileno(), self.size // self.blocksize + 1)

    def _get_need(self, start: int | None, end: int | None) -> list[int]:
        if start is None:
            start = 0
        if end is None:
            end = self.size
        start_block = start // self.blocksize
        end_block = end // self.blocksize
        return [i for i in range(start_block, end_block + 1) if self._index[i] != 2]

    def _wait(self, waiting: list[int], need: list[int]):
        if waiting:
            done = False
            started = datetime.datetime.now()
            while not done and datetime.datetime.now() - started < datetime.timedelta(seconds=30):
                done = True
                for block in waiting:
                    if self._index[block] != 2:
                        done = False
                        time.sleep(0.1)
            if not done:  # Waited for 30 seconds for other processes to finish fetching the needed blocks. Give up and do it ourselves.
                for i in waiting:
                    if self._index[i] != 2:
                        self._index[i] = 0
                        need.append(i)

    async def _await(self, waiting: list[int], need: list[int]):
        if waiting:
            done = False
            started = datetime.datetime.now()
            while not done and datetime.datetime.now() - started < datetime.timedelta(seconds=30):
                done = True
                for block in waiting:
                    if self._index[block] != 2:
                        done = False
                        await asyncio.sleep(0.1)
            if not done:  # Waited for 30 seconds for other processes to finish fetching the needed blocks. Give up and do it ourselves.
                for i in waiting:
                    if self._index[i] != 2:
                        self._index[i] = 0
                        need.append(i)

    def _get_to_fetch(self, need: list[int]) -> Tuple[list[Tuple[int, int, list[int]]], list[int]]:
        waiting: list[int] = []
        to_fetch: list[Tuple[int, int, list[int]]] = []
        while need:
            i = need.pop(0)
            if self._index[i] == 0:
                self._index[i] = 1
                sstart = i * self.blocksize
                cis = [i]
                while need and need[0] == i+1 and self._index[need[0]] == 0:
                    i = need.pop(0)
                    self._index[i] = 1
                    cis.append(i)
                send = min(i * self.blocksize + self.blocksize, self.size)
                to_fetch.append((sstart, send, cis))
            elif self._index[i] != 2:
                waiting.append(i)
        return (to_fetch, waiting)

    def _fetch(self, start: int | None, end: int | None) -> bytes:
        need = self._get_need(start, end)
        while need:
            to_fetch, waiting = self._get_to_fetch(need)
            for sstart, send, cis in to_fetch:
                self.cache[sstart:send] = self.fetcher(sstart, send)
                for i in cis:
                    self._index[i] = 2
            self._wait(waiting, need)
        return self.cache[start:end]

    async def _afetch(self, start: int | None, end: int | None) -> bytes:
        need = self._get_need(start, end)
        while need:
            to_fetch, waiting = self._get_to_fetch(need)
            datas = await asyncio.gather(*[self.afetcher(sstart, send) for sstart, send, _ in to_fetch])  # type: ignore # noqa
            for (sstart, send, cis), data in zip(to_fetch, datas):
                self.cache[sstart:send] = data
                for i in cis:
                    self._index[i] = 2
            await self._await(waiting, need)
        return self.cache[start:end]

    def fill(self, start: int, data: bytes) -> None:
        self.cache[start:start+len(data)] = data
        for i in range(start // self.blocksize, (start + len(data)) // self.blocksize):
            self._index[i] = 2

    def __getstate__(self):
        state = super().__getstate__()
        del state['_index']
        return state

    def __setstate__(self, state: dict[str, Any]):
        super().__setstate__(state)
        self._index = self._makeindex()

    @classmethod
    def register_cache(cls):
        if not cls.name in caches:
            register_cache(cls)


register_cache(SharedMMapCache)


def get_async_filesystem(urlpath: str, storage_options: dict[str, Any] | None = None) -> AsyncFileSystem:
    fs, _, _ = fsspec.get_fs_token_paths(
        urlpath, storage_options=storage_options)
    if isinstance(fs, fsspec.implementations.local.LocalFileSystem):
        fs = AsyncLocalFileSystem()
    if not fs.async_impl:
        raise ValueError("Unsupported non-async filesystem: %s" % fs)
    return fs


def get_cache(fs: AsyncFileSystem, urlpath: str, size: int, cache_dir: str, blocksize: int, parallel_timeout: int, cache_mapper: AbstractCacheMapper) -> SharedMMapCache:
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir, exist_ok=True)

    def _cat_file_fetcher(fs: AsyncFileSystem, urlpath: str, start: int, end: int) -> bytes:
        return fs.cat_file(urlpath, start=start, end=end)  # type: ignore

    async def _cat_file_afetcher(_, urlpath: str, start: int, end: int) -> bytes:
        return await fs._cat_file(urlpath, start=start, end=end)

    return SharedMMapCache(
        blocksize,
        functools.partial(_cat_file_fetcher, fs, urlpath),
        size,
        os.path.join(cache_dir, cache_mapper(urlpath) + ".cache"),
        os.path.join(cache_dir, cache_mapper(urlpath) + ".cache-index"),
        afetcher=functools.partial(_cat_file_afetcher, fs, urlpath),
        parallel_timeout=parallel_timeout)


def prefetch_if_remote(urlpath: str, size: int, cache_dir: str, storage_options: dict[str, Any] | None = None, blocksize: int = 65536, parallel_timeout: int = 30, cache_mapper: AbstractCacheMapper = PathCacheMapper()) -> futures.Future[None]:
    fs = get_async_filesystem(urlpath, storage_options=storage_options)
    if getattr(fs, "local_file", False):
        ret = asyncio.Future()
        ret.set_result(None)
        return ret  # type: ignore
    cache = get_cache(fs, urlpath, size, cache_dir,
                      blocksize, parallel_timeout, cache_mapper)

    async def _a_fill_cache():
        f = await fs.open_async(urlpath, "rb")
        while f.loc < size:
            loc = f.loc
            data = await f.read(block_size*2**4*5)  # type: ignore
            cache.fill(loc, data)
        cache._index[-1] = 2
        await f.close()  # type: ignore
    # type: ignore
    return asyncio.run_coroutine_threadsafe(_a_fill_cache(), fs.loop)


def _get_afetcher(urlpath: str, size: int, storage_options: dict[str, Any] | None = None, parallel_timeout=30, cache_dir: str | None = None, blocksize: int = 65536, cache_mapper: AbstractCacheMapper = PathCacheMapper()):
    fs = get_async_filesystem(urlpath, storage_options=storage_options)
    if cache_dir is None or getattr(fs, "local_file", False):
        return functools.partial(fs._cat_file, urlpath)
    else:
        cache = get_cache(fs, urlpath, size, cache_dir,
                          blocksize, parallel_timeout, cache_mapper)
        return cache._afetch


class PLocalAFetcher:
    def __init__(self, urlpath: str, size: int, storage_options: dict[str, Any] | None = None, parallel_timeout=30, cache_dir: str | None = None, blocksize: int = 65536, cache_mapper: AbstractCacheMapper = PathCacheMapper()):
        self.urlpath = urlpath
        self.size = size
        self.storage_options = storage_options
        self.parallel_timeout = parallel_timeout
        self.cache_dir = cache_dir
        self.blocksize = blocksize
        self.cache_mapper = cache_mapper
        self.plocal = ProcessLocal()

    def __call__(self, offset: int, size: int) -> Coroutine[Any, Any, bytes]:
        if not hasattr(self.plocal, '_afetcher'):
            self.plocal._afetcher = _get_afetcher(
                self.urlpath, self.size, self.storage_options, self.parallel_timeout, self.cache_dir, self.blocksize, self.cache_mapper)
        return self.plocal._afetcher(offset, size)


def get_s3fs_credentials(s3_credentials_yaml_file: str | os.PathLike | None) -> dict[str, str | None]:
    if s3_credentials_yaml_file is None:
        return dict()
    with open(s3_credentials_yaml_file, 'r') as f:
        s3_credentials = yaml.safe_load(f)
        return dict(
            key=s3_credentials['aws_access_key_id'] if 'aws_access_key_id' in s3_credentials else None,
            secret=s3_credentials['aws_secret_access_key'] if 'aws_secret_access_key' in s3_credentials else None,
            endpoint_url=s3_credentials['endpoint_url'] if 'endpoint_url' in s3_credentials else None,
            config_kwargs=dict(max_pool_connections=32)
        )


def cache_locally_if_remote(urlpath: str, storage_options: dict[str, Any] | None = None, cache_dir: str | None = None, cache_mapper: AbstractCacheMapper = PathCacheMapper(), callback=TqdmCallback(tqdm_kwargs=dict(unit='b', unit_scale=True, dynamic_ncols=True))) -> str:
    fs = get_async_filesystem(urlpath, storage_options=storage_options)
    if getattr(fs, "local_file", False):
        return urlpath
    if cache_dir is None:
        raise ValueError(
            "If you want to use a non-local filesystem, you need to specify a cache_dir")
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir, exist_ok=True)
    lpath = os.path.join(
        cache_dir, cache_mapper(urlpath))
    if not os.path.exists(lpath):
        fs.get_file(urlpath, lpath, callback=callback)  # type: ignore
    return lpath


def get_as_locally_cached_filesystem_if_remote(urlpath: str, storage_options: dict[str, Any] | None = None, cache_dir: str | None = None, cache_mapper: AbstractCacheMapper = PathCacheMapper()):
    fs = get_async_filesystem(urlpath, storage_options=storage_options)
    if getattr(fs, "local_file", False):
        return fs
    if cache_dir is None:
        raise ValueError(
            "If you want to use a non-local filesystem, you need to specify a cache_dir")
    return SimpleCacheFileSystem(fs=fs, cache_storage=cache_dir, cache_mapper=cache_mapper)


async def _fetch_async(afetcher: AFetcher, offsets_and_sizes: Iterable[Tuple[int, int]]) -> list[bytes]:
    return await asyncio.gather(*[afetcher(offset, size) for offset, size in offsets_and_sizes])


def fetch_async(afetcher: AFetcher, offsets_and_sizes: Iterable[Tuple[int, int]]) -> list[bytes]:
    ret = asyncio.run_coroutine_threadsafe(_fetch_async(
        afetcher, offsets_and_sizes), fsspec.asyn.get_loop()).result()
    return ret

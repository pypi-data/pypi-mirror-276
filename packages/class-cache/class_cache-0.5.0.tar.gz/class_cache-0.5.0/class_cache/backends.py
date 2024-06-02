# ruff: noqa: S608
import codecs
import json
import pickle  # noqa: S403
import sqlite3
from abc import ABC
from collections import defaultdict
from pathlib import Path
from typing import Any, Iterable, Iterator, MutableMapping, TypeAlias, cast

import brotli
from marisa_trie import Trie
from replete.consistent_hash import consistent_hash
from replete.flock import FileLock

from class_cache.types import KeyType, ValueType
from class_cache.utils import get_class_cache_dir

ID_TYPE: TypeAlias = str | int | None


class BaseBackend(ABC, MutableMapping[KeyType, ValueType]):
    def __init__(self, id_: ID_TYPE = None) -> None:
        self._id = id_

    @property
    def id(self) -> ID_TYPE:
        return self._id

    # Override these methods to allow getting results in a more optimal fashion
    def contains_many(self, keys: Iterable[KeyType]) -> Iterator[tuple[KeyType, bool]]:
        for key in keys:
            yield key, key in self

    def get_many(self, keys: Iterable[KeyType]) -> Iterator[tuple[KeyType, ValueType]]:
        for key in keys:
            yield key, self[key]

    def set_many(self, items: Iterable[tuple[KeyType, ValueType]]) -> None:
        for key, value in items:
            self[key] = value

    def del_many(self, keys: Iterable[KeyType]) -> None:
        for key in keys:
            del self[key]

    def clear(self) -> None:
        self.del_many(self)


class PickleBackend(BaseBackend[KeyType, ValueType]):
    ROOT_DIR = get_class_cache_dir() / "PickleBackend"
    BLOCK_SUFFIX = ".block.pkl"
    META_TYPE = dict[str, Any]

    def __init__(self, id_: ID_TYPE = None, max_block_size=1024 * 1024) -> None:
        super().__init__(id_)
        self._dir = self.ROOT_DIR / str(self.id)
        self._dir.mkdir(exist_ok=True, parents=True)
        self._max_block_size = max_block_size
        self._meta_path = self._dir / "meta.json"
        self._lock = FileLock(self._meta_path)
        self._check_meta()

    @property
    def dir(self) -> Path:
        return self._dir

    # Helper methods, they don't acquire locks, so should only be used inside methods that do
    def _read_meta(self) -> META_TYPE:
        with self._meta_path.open() as f:
            return json.load(f)

    def _write_meta(self, meta: META_TYPE) -> None:
        with self._meta_path.open("w") as f:
            json.dump(meta, f)

    def _write_clean_meta(self) -> None:
        self._write_meta({"len": 0})

    def get_path_for_block_id(self, block_id: str) -> Path:
        return self._dir / f"{block_id}{self.BLOCK_SUFFIX}"

    def _get_key_hash(self, key: KeyType) -> str:
        return f"{consistent_hash(key):x}"

    def _get_block_id_for_key(self, key: KeyType, prefix_len=1) -> str:
        key_hash = self._get_key_hash(key)

        blocks_trie = Trie(self.get_all_block_ids())
        prefixes = blocks_trie.prefixes(key_hash)
        if prefix_len > len(key_hash):
            raise ValueError("Got prefix_len that is larger than key_hash len.")
        return key_hash[:prefix_len] if not prefixes else max(prefixes, key=len)

    def _get_block(self, block_id: str) -> dict[KeyType, ValueType]:
        try:
            with self.get_path_for_block_id(block_id).open("rb") as f:
                return pickle.load(f)  # noqa: S301
        except FileNotFoundError:
            return {}

    def _write_block(self, block_id: str, block: dict[KeyType, ValueType]) -> None:
        with self.get_path_for_block_id(block_id).open("wb") as f:
            pickle.dump(block, f, pickle.HIGHEST_PROTOCOL)

    def _update_length(self, change: int) -> None:
        meta = self._read_meta()
        meta["len"] += change
        self._write_meta(meta)

    def _get_block_for_key(self, key: KeyType) -> dict[KeyType, ValueType]:
        return self._get_block(self._get_block_id_for_key(key))

    def get_all_block_ids(self) -> Iterable[str]:
        with self._lock.read_lock():
            yield from (path.name.split(".")[0] for path in self._dir.glob(f"*{self.BLOCK_SUFFIX}"))

    def _check_meta(self) -> None:
        with self._lock.read_lock():
            if self._meta_path.exists():
                return
            if list(self.get_all_block_ids()):
                raise ValueError(f"Found existing blocks without meta file in {self._dir}")
        with self._lock.write_lock():
            self._write_clean_meta()

    def __contains__(self, key: KeyType) -> bool:
        with self._lock.read_lock():
            return key in self._get_block_for_key(key)

    def __len__(self) -> int:
        with self._lock.read_lock():
            return self._read_meta()["len"]

    def __iter__(self) -> Iterator[KeyType]:
        # TODO: Optimise this
        with self._lock.read_lock():
            for block_id in self.get_all_block_ids():
                yield from self._get_block(block_id).keys()

    def __getitem__(self, key: KeyType) -> ValueType:
        with self._lock.read_lock():
            return self._get_block_for_key(key)[key]

    def __setitem__(self, key: KeyType, value: ValueType, prefix_len=1) -> None:
        with self._lock.write_lock():
            block_id = self._get_block_id_for_key(key, prefix_len=prefix_len)
            block = self._get_block(block_id)
            change = 0 if key in block else 1
            block[key] = value
            self._write_block(block_id, block)
            self._update_length(change)

        if self.get_path_for_block_id(block_id).stat().st_size > self._max_block_size:
            self._split_block(block_id)

    def _split_block(self, block_id: str) -> None:
        with self._lock.write_lock():
            block = self._get_block(block_id)
            self.get_path_for_block_id(block_id).unlink()
            new_prefix_len = len(block_id) + 1
            new_blocks = defaultdict(dict)
            for key, value in block.items():
                new_blocks[self._get_block_id_for_key(key, new_prefix_len)][key] = value
            for new_block_id, new_block in new_blocks.items():
                self._write_block(new_block_id, new_block)

    def __delitem__(self, key: KeyType) -> None:
        with self._lock.write_lock():
            block_id = self._get_block_id_for_key(key)
            block = self._get_block(block_id)
            del block[key]
            self._write_block(block_id, block)
            self._update_length(-1)

    def clear(self) -> None:
        with self._lock.write_lock():
            for block_id in self.get_all_block_ids():
                self.get_path_for_block_id(block_id).unlink()
            self._meta_path.unlink()
            self._write_clean_meta()


class SQLiteBackend(BaseBackend[KeyType, ValueType]):
    ROOT_DIR = get_class_cache_dir() / "SQLiteBackend"
    ROOT_DIR.mkdir(parents=True, exist_ok=True)
    DATA_TABLE_NAME = "data"

    def __init__(self, id_: ID_TYPE = None) -> None:
        super().__init__(id_)
        self._db_path = self.ROOT_DIR / f"{self.id}.db"
        self._con = sqlite3.connect(self._db_path)
        self._cursor = self._con.cursor()
        self._check_table()

    @property
    def db_path(self) -> Path:
        return self._db_path

    def _check_table(self):
        tables = self._cursor.execute("SELECT name FROM sqlite_master LIMIT 1").fetchone()
        if tables is None:
            self._cursor.execute(f"CREATE TABLE {self.DATA_TABLE_NAME}(key TEXT, value TEXT)")
            self._cursor.execute(f"CREATE UNIQUE INDEX key_index ON {self.DATA_TABLE_NAME}(key)")

    # TODO: Can probably cache these
    def _encode(self, obj: KeyType | ValueType) -> str:
        return codecs.encode(pickle.dumps(obj), "base64").decode()

    def _decode(self, stored: str) -> KeyType | ValueType:
        return pickle.loads(codecs.decode(stored.encode(), "base64"))  # noqa: S301

    def __contains__(self, key: KeyType) -> bool:
        key_str = self._encode(key)
        sql = f"SELECT EXISTS(SELECT 1 FROM {self.DATA_TABLE_NAME} WHERE key=? LIMIT 1)"
        value = self._cursor.execute(sql, (key_str,)).fetchone()[0]
        return value != 0

    def __len__(self) -> int:
        return self._cursor.execute(f"SELECT COUNT(key) FROM {self.DATA_TABLE_NAME}").fetchone()[0]

    def __iter__(self) -> Iterator[KeyType]:
        for key_str in self._cursor.execute(f"SELECT key FROM {self.DATA_TABLE_NAME}").fetchall():
            yield cast(KeyType, self._decode(key_str[0]))

    def __getitem__(self, key: KeyType) -> ValueType:
        key_str = self._encode(key)
        sql = f"SELECT value FROM {self.DATA_TABLE_NAME} WHERE key=? LIMIT 1"
        res = self._cursor.execute(sql, (key_str,)).fetchone()
        if res is None:
            raise KeyError(key)
        return cast(ValueType, self._decode(res[0]))

    def __setitem__(self, key: KeyType, value: ValueType) -> None:
        key_str = self._encode(key)
        value_str = self._encode(value)
        self._cursor.execute(f"INSERT INTO {self.DATA_TABLE_NAME} VALUES (?, ?)", (key_str, value_str))
        self._con.commit()

    def __delitem__(self, key: KeyType) -> None:
        key_str = self._encode(key)
        self._cursor.execute(f"DELETE FROM {self.DATA_TABLE_NAME} WHERE key=?", (key_str,))
        self._con.commit()

    def clear(self) -> None:
        self._cursor.execute(f"DROP TABLE IF EXISTS {self.DATA_TABLE_NAME}")
        self._con.commit()
        self._check_table()

    def __del__(self):
        self._con.commit()
        self._con.close()

    # TODO: implement *_many methods


class BackendWrapper(BaseBackend[KeyType, ValueType]):
    """
    :param backend: backend to be wrapped
    """

    def __init__(self, *args, backend_type: type[BaseBackend], **kwargs) -> None:
        super().__init__()
        self._backend = backend_type(*args, **kwargs)

    def __contains__(self, key: KeyType) -> bool:
        return key in self._backend

    def __len__(self) -> int:
        return len(self._backend)

    def __iter__(self) -> Iterator[KeyType]:
        yield from self._backend

    def __getitem__(self, key: KeyType) -> ValueType:
        return self._backend[key]

    def __setitem__(self, key: KeyType, value: ValueType) -> None:
        self._backend[key] = value

    def __delitem__(self, key: KeyType) -> None:
        del self._backend[key]

    def contains_many(self, keys: Iterable[KeyType]) -> Iterator[tuple[KeyType, bool]]:
        yield from self._backend.contains_many(keys)

    def get_many(self, keys: Iterable[KeyType]) -> Iterator[tuple[KeyType, ValueType]]:
        yield from self._backend.get_many(keys)

    def set_many(self, items: Iterable[tuple[KeyType, ValueType]]) -> None:
        self._backend.set_many(items)

    def del_many(self, keys: Iterable[KeyType]) -> None:
        self._backend.del_many(keys)

    def clear(self) -> None:
        self._backend.clear()


class BrotliCompressWrapper(BackendWrapper[KeyType, ValueType]):
    def _encode(self, obj: KeyType | ValueType) -> bytes:
        return brotli.compress(pickle.dumps(obj, pickle.HIGHEST_PROTOCOL))

    def _decode(self, stored: bytes) -> KeyType | ValueType:
        return pickle.loads(brotli.decompress(stored))  # noqa: S301

    def __contains__(self, key: KeyType) -> bool:
        return super().__contains__(key)

    def __iter__(self) -> Iterator[KeyType]:
        yield from super().__iter__()

    def __getitem__(self, key: KeyType) -> ValueType:
        return self._decode(super().__getitem__(key))

    def __setitem__(self, key: KeyType, value: ValueType) -> None:
        self._backend[key] = self._encode(value)

    def __delitem__(self, key: KeyType) -> None:
        return super().__delitem__(key)

    def set_many(self, items: Iterable[tuple[KeyType, ValueType]]) -> None:
        return super().set_many((key, self._encode(value)) for key, value in items)

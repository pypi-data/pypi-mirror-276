import asyncio

from collections.abc import MutableMapping
from typing import (
    Any, Generic, Iterable, Iterator, Type, TypeVar, TypedDict, overload
)


_K = TypeVar("_K")
_V = TypeVar("_V")


class TestMemoryKeyMeta(TypedDict):
    """Metadata for a key in the test memory dictionary."""
    dtype: set[Type] | None
    """The data type(s) of the values associated with the key."""
    updatable: bool
    """If False, the value associated with the key cannot be overwritten."""
    lock: asyncio.Lock
    """An asyncio lock for the key to ensure data consistency."""


class TestMemoryKeyData(TypedDict, Generic[_V]):
    """Data for a key in the test memory dictionary."""
    value: _V | None
    """The value associated with the key. If None, the key has no value set."""
    history: list[_V] | None
    """A list of previous values for the key. If None, no history is stored."""
    meta: TestMemoryKeyMeta
    """The metadata dict for the key."""


class TestMemory(MutableMapping[_K, _V], Generic[_K, _V]):
    """
    A mapping-like structure for storing data collected during a test run.
    Provides basic functionality to create, read, write, and clear key-value
    pairs as well as additional features such as storing previous values for
    a key, managing data types, ensuring data consistency, and providing
    asynchronous access to the data.
    """

    def __init__(self) -> None:
        self.__memory: dict[_K, TestMemoryKeyData[_V]] = {}
        self.__memory_lock = asyncio.Lock()

    def __str__(self) -> str:
        return str(dict(self))

    def __repr__(self) -> str:
        return str(dict(self))

    def __getitem__(self, key: _K) -> _V:
        value = self.__memory[key]['value']
        if value is None:
            raise KeyError(f'Key "{key}" has no value assigned.')
        return value

    def __setitem__(self, key: _K, value: _V) -> None:
        if key in self.__memory:
            self._set_value(value, self._get_keydata(key), force_update=False)
        else:
            self.new_key(key, value=value)

    def __delitem__(self, key: _K) -> None:
        del self.__memory[key]

    def __iter__(self) -> Iterator[_K]:
        return iter(self.__memory)

    def __len__(self) -> int:
        return len(self.__memory)

    def _format_dtype(self, dtype: Any) -> set[Type] | None:
        """Format the data type(s) for a key value to a set of types or None.

        Args:
            dtype (Any): The data type(s) to be formatted.

        Raises:
            TypeError: If the data type is not a type or an iterable of types.

        Returns:
            set[Type] | None: The formatted data type(s) as a set of types\
                or None.
        """
        if dtype is None:
            return None
        if isinstance(dtype, Iterable) and not isinstance(dtype, str):
            dtype = set(t for t in dtype)
        else:
            dtype = set((dtype,))
        for t in dtype:
            if not isinstance(t, type):
                raise TypeError(
                    f'Invalid data type "{t}". Expected a type, '
                    f'got an object instance of type "{type(t).__name__}".'
                )
        return dtype

    def _validate_value(
        self, value: _V | None, keymeta: TestMemoryKeyMeta
    ) -> None:
        """Ensure that the value is of the correct data type for the key.

        Args:
            value (_V | None): The value to be validated.
            keymeta (TestMemoryKeyMeta): The metadata for the key associated\
                with the value.

        Raises:
            TypeError: If the value is not of the correct data type.
        """
        if value is None:
            return
        allowed_types = keymeta['dtype']
        if not allowed_types:
            return
        if any(isinstance(value, t) for t in allowed_types):
            return
        allowed_types_str = ', '.join(f'"{t.__name__}"' for t in allowed_types)
        raise TypeError(
            f'Invalid value "{value}" of type "{type(value).__name__}". '
            f'Expected a value of type(s) {allowed_types_str}.'
            )

    def _get_keydata(self, key: _K) -> TestMemoryKeyData[_V]:
        """Retrieve the data associated with the specified key from the memory
        dictionary.

        Args:
            key (_K): The key for which to retrieve the data.

        Raises:
            KeyError: If the key is not present in the memory dictionary.

        Returns:
            TestMemoryKeyData[_V]: The data associated with the key.
        """
        if key not in self.__memory:
            raise KeyError(f'Key "{key}" is not present in the test memory.')
        return self.__memory[key]

    def _set_value(
        self, value: _V, keydata: TestMemoryKeyData, force_update: bool
    ) -> None:
        """Set the value for the specified key in the memory dictionary.

        Args:
            value (_V): The value to be set for the key.
            keydata (TestMemoryKeyData): The data associated with the key.
            force_update (bool): If True, allows updating a non-updatable key.

        Raises:
            KeyError: If the key is not updatable and the "force_update"\
                parameter is set to False.
        """
        self._validate_value(value, keydata['meta'])
        value_prev = keydata['value']
        if value_prev is not None:
            if not keydata['meta']['updatable'] and not force_update:
                raise KeyError(
                    f'Cannot set updatable key value to "{value}".'
                    )
            if keydata['history'] is not None:
                keydata['history'].append(value_prev)
        keydata['value'] = value

    def new_key(
        self,
        key: _K,
        value: _V | None = None,
        dtype: Type | Iterable[Type] | None = None,
        history: bool = False,
        updatable: bool = True,
        overwrite: bool = False
    ) -> None:
        """Create a new key in the memory dictionary with optional data type
        and storage settings.

        Args:
            key (_K): The key to be created.
            value (_V, optional): The value to be associated with the key.
            dtype (Type | Iterable[Type] | None, optional): The data type\
                of the values associated with the key. If None, the value\
                associated with the key may have any value type(s).\
                Defaults to None.
            history (bool, optional): If True, previous values for this key\
                will be stored when new values are written. Defaults to False.
            updatable (bool, optional): If False, the value associated with\
                the key cannot be overwritten accidentally. Defaults to False.
            overwrite (bool, optional): If True, the key will be overwritten\
                if it already exists in the memory dictionary.\
                Defaults to False.

        Raises:
            KeyError: If the key already exists in the memory dictionary and\
                the "overwrite" parameter is set to False.
        """
        if key in self.__memory and not overwrite:
            raise KeyError(f'Key "{key}" already exists in the test memory.')
        keymeta: TestMemoryKeyMeta = {
            'dtype': self._format_dtype(dtype),
            'updatable': updatable,
            'lock': asyncio.Lock()
            }
        if value is not None:
            self._validate_value(value, keymeta)
        self.__memory[key] = {
            'value': value,
            'history': [] if history else None,
            'meta': keymeta
            }

    @overload
    async def read(self, key: _K, depth: None) -> _V | None: ...

    @overload
    async def read(self, key: _K, depth: int) -> list[_V]: ...

    async def read(
        self, key: _K, depth: int | None = None
    ) -> _V | list[_V] | None:
        """Retrieve the value associated with the specified key from the memory
        dictionary.

        This method acts as a standard dictionary read operation, but is also
        asynchronous and should be used in an asynchronous context. The method
        can also retrieve a specified number of previous values for the key
        if the "depth" parameter is set to a positive integer and the key has
        a history of previous values.

        Args:
            key (_K): The key for which to retrieve the value.
            depth (int | None, optional): The number of previous values to\
                retrieve for the key. If None, only the current value\
                is returned. Defaults to None.

        Returns:
            _V | list[_V] | None: The value associated with the key.\
                If the "depth" parameter is set to a positive integer,\
                a list of the previous values for the key will be returned.

        Raises:
            KeyError: If the key is not present in the test memory.
        """
        async with self.__memory_lock:
            keydata = self._get_keydata(key)
        async with keydata['meta']['lock']:
            value = keydata['value']
            if value is None:
                return None
            if depth is None:
                return value
            history = keydata['history']
            if history is None:
                return [value]
            if depth < 1:
                return [value]
            return history[-depth:] + [value]

    async def write(
        self, key: _K, value: _V, force_update: bool = False
    ) -> None:
        """
        Write a value to the specified key in the memory dictionary.

        This method acts as a standard dictionary write operation, but is also
        asynchronous and should be used in an asynchronous context.

        Args:
            key (_K): The key to write the value to.
            value (_V): The value to be written to the key.
            force_update (bool, optional): If set to True,\
                allows updating a non-updatable key. Defaults to False.

        Raises:
            KeyError: if attempting to reassign a non-updatable key\
                without setting the "force_update" parameter to True.
        """
        async with self.__memory_lock:
            if key not in self.__memory:
                self.new_key(key, value)
                return
            else:
                keydata = self._get_keydata(key)
        async with keydata['meta']['lock']:
            self._set_value(value, keydata, force_update)

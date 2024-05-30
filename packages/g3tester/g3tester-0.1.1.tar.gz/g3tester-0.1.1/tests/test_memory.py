import pytest

from ._memory import TestMemory


@pytest.fixture
def test_memory():
    return TestMemory()


def test_new_key(test_memory):
    test_memory.new_key('key1', value=10)
    assert test_memory['key1'] == 10


def test_set_value(test_memory):
    test_memory.new_key('key1', value=10)
    test_memory['key1'] = 20
    assert test_memory['key1'] == 20


def test_del_item(test_memory):
    test_memory.new_key('key1', value=10)
    del test_memory['key1']
    with pytest.raises(KeyError):
        test_memory['key1']


def test_iter(test_memory):
    test_memory.new_key('key1', value=10)
    test_memory.new_key('key2', value=20)
    assert set(test_memory) == {'key1', 'key2'}


def test_len(test_memory):
    test_memory.new_key('key1', value=10)
    test_memory.new_key('key2', value=20)
    assert len(test_memory) == 2


@pytest.mark.asyncio
async def test_read(test_memory):
    test_memory.new_key('key1', value=10, history=True)
    test_memory['key1'] = 20
    test_memory['key1'] = 30
    assert await test_memory.read('key1') == 30
    assert await test_memory.read('key1', depth=2) == [10, 20, 30]


@pytest.mark.asyncio
async def test_write(test_memory):
    test_memory.new_key('key1', value=10)
    await test_memory.write('key1', 20)
    assert test_memory['key1'] == 20


@pytest.mark.asyncio
async def test_write_non_updatable(test_memory):
    test_memory.new_key('key1', value=10, updatable=False)
    with pytest.raises(KeyError):
        await test_memory.write('key1', 20)


@pytest.mark.asyncio
async def test_write_force_update(test_memory):
    test_memory.new_key('key1', value=10, updatable=False)
    await test_memory.write('key1', 20, force_update=True)
    assert test_memory['key1'] == 20

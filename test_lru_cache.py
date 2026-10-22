import pytest

from lru_cache import LRUCache


def test_basic_eviction_order():
    cache = LRUCache(2)
    cache.put(1, 1)
    cache.put(2, 2)
    assert cache.get(1) == 1   # 1 is now most recent
    cache.put(3, 3)            # evicts 2
    assert cache.get(2) == -1
    cache.put(4, 4)            # evicts 1
    assert cache.get(1) == -1
    assert cache.get(3) == 3
    assert cache.get(4) == 4


def test_update_existing_key_does_not_evict():
    cache = LRUCache(2)
    cache.put("a", 1)
    cache.put("b", 2)
    cache.put("a", 10)         # update, and "a" becomes most recent
    assert len(cache) == 2
    cache.put("c", 3)          # evicts "b"
    assert cache.get("a") == 10
    assert cache.get("b") == -1
    assert cache.get("c") == 3


def test_capacity_one():
    cache = LRUCache(1)
    cache.put(1, 1)
    cache.put(2, 2)
    assert cache.get(1) == -1
    assert cache.get(2) == 2


def test_missing_key():
    assert LRUCache(3).get("nope") == -1


@pytest.mark.parametrize("capacity", [0, -1])
def test_invalid_capacity(capacity):
    with pytest.raises(ValueError):
        LRUCache(capacity)

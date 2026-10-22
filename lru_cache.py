"""Problem 1: LRU Cache with O(1) get and put."""


class _Node:
    __slots__ = ("key", "value", "prev", "next")

    def __init__(self, key=None, value=None):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None


class LRUCache:
    """Hash map (key -> node) + doubly linked list ordered by recency.

    head.next is the most recently used node, tail.prev the least recently used.
    """

    def __init__(self, capacity: int):
        if capacity < 1:
            raise ValueError("capacity must be a positive integer")
        self.capacity = capacity
        self.map = {}
        # Sentinel nodes so insert/remove never have to handle None neighbours.
        self.head = _Node()
        self.tail = _Node()
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node: _Node) -> None:
        node.prev.next = node.next
        node.next.prev = node.prev

    def _add_to_front(self, node: _Node) -> None:
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node

    def get(self, key):
        node = self.map.get(key)
        if node is None:
            return -1
        # Mark as most recently used.
        self._remove(node)
        self._add_to_front(node)
        return node.value

    def put(self, key, value) -> None:
        node = self.map.get(key)
        if node is not None:
            node.value = value
            self._remove(node)
            self._add_to_front(node)
            return

        node = _Node(key, value)
        self.map[key] = node
        self._add_to_front(node)

        if len(self.map) > self.capacity:
            lru = self.tail.prev
            self._remove(lru)
            del self.map[lru.key]

    def __len__(self) -> int:
        return len(self.map)

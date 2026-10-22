# Avaloka AI Assignment

Prakhar Saxena

## Problem 1: LRU Cache

### Approach

I used a hash map together with a doubly linked list. The map goes from key to a node in the list, so I can find any entry in O(1). The list keeps the order of use: the node right after head is the most recently used and the node right before tail is the least recently used.

On get, I look up the node in the map, move it to the front of the list and return its value, or return -1 if the key isn't there. On put, if the key exists I update the value and move it to the front. Otherwise I add a new node at the front, and if the cache goes over capacity I remove the node before tail from both the list and the map.

I chose these structures because each one covers what the other is bad at. A hash map alone has no order, and a list alone needs O(n) to find a key. The list needs to be doubly linked so I can unlink a node from the middle without walking the list to find the node before it. I also used dummy head and tail nodes so I don't need special cases for an empty list, and each node stores its key so I know what to delete from the map when evicting.

### Code

```python
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
```

## Problem 2: Event Scheduler

### Approach

For can_attend_all, I sort the events by start time and check that each event starts no earlier than the previous one ends. If one starts before the previous one ends, there is an overlap. The check uses a strict less-than, so back-to-back events like (9, 10) and (10, 11) are allowed.

For min_rooms_required, I sort by start time and keep a min-heap of end times for the rooms currently in use. For each event, if the earliest end time in the heap is less than or equal to the event's start, that room is free, so I pop it. Then I push the new event's end time. The heap size is the number of rooms in use at that moment, and the largest size it reaches is the answer. Looking only at the earliest end time is enough, because if that meeting hasn't finished, none of the others have either.

### Code

```python
"""Problem 2: Event Scheduler."""

import heapq


def _validate(events):
    for start, end in events:
        if start >= end:
            raise ValueError(f"invalid event ({start}, {end}): start must be before end")


def can_attend_all(events) -> bool:
    """True if no two events overlap. Touching events (end == start) are allowed."""
    _validate(events)
    ordered = sorted(events)
    for i in range(1, len(ordered)):
        # Strict '<' so (9, 10) and (10, 11) do not count as overlapping.
        if ordered[i][0] < ordered[i - 1][1]:
            return False
    return True


def min_rooms_required(events) -> int:
    """Minimum number of rooms needed to host every event."""
    _validate(events)
    ordered = sorted(events)
    end_times = []  # min-heap: end time of each room currently in use
    max_rooms = 0
    for start, end in ordered:
        # The earliest-ending meeting is over, so reuse its room.
        if end_times and end_times[0] <= start:
            heapq.heappop(end_times)
        heapq.heappush(end_times, end)
        max_rooms = max(max_rooms, len(end_times))
    return max_rooms


def _room_name(index: int) -> str:
    """0 -> 'Room A', 25 -> 'Room Z', 26 -> 'Room AA', ..."""
    letters = ""
    index += 1
    while index:
        index, rem = divmod(index - 1, 26)
        letters = chr(ord("A") + rem) + letters
    return f"Room {letters}"


def assign_rooms(events) -> dict:
    """Future-proofing extension: map each event to a specific room name.

    Freed rooms are reused lowest-letter first, so the same rooms stay busy.
    """
    _validate(events)
    ordered = sorted(events)
    busy = []       # min-heap of (end_time, room_index)
    free = []       # min-heap of room indexes that are currently free
    next_room = 0
    assignment = {}
    for start, end in ordered:
        while busy and busy[0][0] <= start:
            _, room = heapq.heappop(busy)
            heapq.heappush(free, room)
        if free:
            room = heapq.heappop(free)
        else:
            room = next_room
            next_room += 1
        heapq.heappush(busy, (end, room))
        assignment.setdefault((start, end), []).append(_room_name(room))
    return assignment
```

## Final Discussion & Analysis

### Time & Space Complexity

LRU cache: get and put are both O(1) time, since each is one hash map lookup plus a few pointer changes. The cache uses O(capacity) space.

can_attend_all: O(n log n) time for the sort, and the scan after it is O(n). Space is O(n) for the sorted copy.

min_rooms_required: O(n log n) time. Sorting is O(n log n), and each event is pushed and popped at most once at O(log n) each. Space is O(n) for the heap in the worst case, when all events overlap.

(assign_rooms, the extra function for room names, is also O(n log n) time and O(n) space.)

### Trade-offs

A hash map gives O(1) lookup but doesn't keep any order, so finding the least recently used item would take O(n). A linked list keeps order but finding a key in it is O(n). Using both gives O(1) for get and put. It has to be doubly linked, because removing a node from a singly linked list needs the previous node. An array would need shifting every time an item moves. The downside is extra memory for the pointers and stored keys, and the pointer code is a bit easy to get wrong. Python's OrderedDict works the same way internally and could be used instead.

### Future Proofing

To assign room names, I'd store (end_time, room_id) in the heap instead of just end times, and keep a second min-heap of free room IDs. Before placing each event, I move any rooms that have finished into the free heap. Then I give the event the lowest free room, or open a new one if none are free. I've written this as assign_rooms in scheduler.py, with names going Room A, Room B, and so on. It's still O(n log n).

### Concurrency

The cache isn't thread-safe as written, because even get changes the list. If two threads move nodes at the same time, they can break the pointers or leave the map and list out of sync. The simple fix is to add a threading.Lock and hold it for all of get and put. A read-write lock wouldn't help much, since get also writes. If the single lock became a bottleneck, the cache could be split into several shards, each with its own lock, picked by hashing the key. That reduces contention, but eviction becomes per-shard instead of a true global LRU.

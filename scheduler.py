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

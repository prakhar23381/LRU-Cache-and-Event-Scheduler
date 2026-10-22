import pytest

from scheduler import assign_rooms, can_attend_all, min_rooms_required


def test_example_input_adjacent_events():
    events = [(9, 10), (10, 11), (11, 12)]
    assert can_attend_all(events) is True
    assert min_rooms_required(events) == 1


def test_overlap_classic():
    events = [(0, 30), (5, 10), (15, 20)]
    assert can_attend_all(events) is False
    assert min_rooms_required(events) == 2


def test_unsorted_input():
    events = [(11, 12), (9, 10), (10, 11)]
    assert can_attend_all(events) is True
    assert min_rooms_required(events) == 1


def test_fully_nested():
    events = [(1, 10), (2, 9), (3, 8), (4, 7)]
    assert min_rooms_required(events) == 4


def test_same_end_time():
    events = [(1, 5), (2, 5), (3, 5), (5, 6)]
    assert min_rooms_required(events) == 3


def test_empty_and_single():
    assert can_attend_all([]) is True
    assert min_rooms_required([]) == 0
    assert can_attend_all([(1, 2)]) is True
    assert min_rooms_required([(1, 2)]) == 1


def test_invalid_event():
    with pytest.raises(ValueError):
        min_rooms_required([(5, 5)])


def test_assign_rooms_reuses_lowest_room():
    events = [(0, 30), (5, 10), (15, 20)]
    assert assign_rooms(events) == {
        (0, 30): ["Room A"],
        (5, 10): ["Room B"],
        (15, 20): ["Room B"],
    }


def test_assign_rooms_count_matches_min_rooms():
    events = [(1, 4), (2, 5), (7, 9), (3, 6), (4, 8), (6, 10)]
    rooms = {r for names in assign_rooms(events).values() for r in names}
    assert len(rooms) == min_rooms_required(events)

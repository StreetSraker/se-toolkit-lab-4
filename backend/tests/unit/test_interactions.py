"""Unit tests for interaction filtering logic."""

from app.models.interaction import InteractionLog
from app.routers.interactions import _filter_by_item_id


def _make_log(id: int, learner_id: int, item_id: int) -> InteractionLog:
    return InteractionLog(id=id, learner_id=learner_id, item_id=item_id, kind="attempt")


def test_filter_returns_all_when_item_id_is_none() -> None:
    interactions = [_make_log(1, 1, 1), _make_log(2, 2, 2)]
    result = _filter_by_item_id(interactions, None)
    assert result == interactions


def test_filter_returns_empty_for_empty_input() -> None:
    result = _filter_by_item_id([], 1)
    assert result == []


def test_filter_returns_interaction_with_matching_ids() -> None:
    interactions = [_make_log(1, 1, 1), _make_log(2, 2, 2)]
    result = _filter_by_item_id(interactions, 1)
    assert len(result) == 1
    assert result[0].id == 1


def test_filter_excludes_interaction_with_different_learner_id() -> None:
    interactions = [_make_log(1, 1, 1), _make_log(2, 2, 1)]
    result = _filter_by_item_id(interactions, 1)
    assert len(result) == 2
    assert result[0].id == 1
    assert result[1].id == 2


def test_filter_with_negative_item_id() -> None:
    interactions = [_make_log(1, 1, -1), _make_log(2, 2, 1)]
    result = _filter_by_item_id(interactions, -1)
    assert len(result) == 1
    assert result[0].id == 1


def test_filter_with_zero_item_id() -> None:
    interactions = [_make_log(1, 1, 0), _make_log(2, 2, 1)]
    result = _filter_by_item_id(interactions, 0)
    assert len(result) == 1
    assert result[0].id == 1


def test_filter_returns_multiple_matches_same_item_id() -> None:
    interactions = [
        _make_log(1, 1, 1),
        _make_log(2, 2, 1),
        _make_log(3, 3, 1),
        _make_log(4, 1, 2),
    ]
    result = _filter_by_item_id(interactions, 1)
    assert len(result) == 3
    assert [i.id for i in result] == [1, 2, 3]


def test_filter_with_large_item_id() -> None:
    large_id = 2**31 - 1  # Max 32-bit signed int
    interactions = [_make_log(1, 1, large_id), _make_log(2, 2, 1)]
    result = _filter_by_item_id(interactions, large_id)
    assert len(result) == 1
    assert result[0].id == 1


def test_filter_preserves_all_kinds_when_filtering_by_item_id() -> None:
    interactions = [
        _make_log(1, 1, 1),
        _make_log(2, 1, 1),
        _make_log(3, 1, 2),
    ]
    interactions[0].kind = "attempt"
    interactions[1].kind = "view"
    interactions[2].kind = "attempt"
    result = _filter_by_item_id(interactions, 1)
    assert len(result) == 2
    assert set(i.kind for i in result) == {"attempt", "view"}
    



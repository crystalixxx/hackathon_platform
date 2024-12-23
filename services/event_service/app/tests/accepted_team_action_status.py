from datetime import datetime, timezone

import pytest
from unittest.mock import AsyncMock, MagicMock
from fastapi import HTTPException
from pydantic import ValidationError

from services.event_service.app.database.schemas.accepted_team_action_status import ActionStatusBase, \
    ActionStatusCreate, AcceptedTeamActionStatusSchema, ActionStatusUpdate


def test_create_action_status_base():
    data = {"track_team_id": 1, "timeline_id": 2}
    action_status = ActionStatusBase(**data)

    assert action_status.track_team_id == 1
    assert action_status.timeline_id == 2
    assert action_status.result_value is None
    assert action_status.resolution_link is None
    assert action_status.completed_at is not None
    assert action_status.notes is None


def test_create_action_status_base_with_all_data():
    now = datetime.now(timezone.utc)
    data = {
        "track_team_id": 1,
        "timeline_id": 2,
        "result_value": "Success",
        "resolution_link": "http://example.com",
        "completed_at": now,
        "notes": "notes",
    }
    action_status = ActionStatusBase(**data)

    assert action_status.track_team_id == 1
    assert action_status.timeline_id == 2
    assert action_status.result_value == "Success"
    assert action_status.resolution_link == "http://example.com"
    assert action_status.completed_at == now
    assert action_status.notes == "notes"


def test_create_action_status_create():
    data = {"track_team_id": 1, "timeline_id": 2}
    action_status = ActionStatusCreate(**data)

    assert action_status.track_team_id == 1
    assert action_status.timeline_id == 2


def test_create_accepted_team_action_status_schema():
    now = datetime.now(timezone.utc)
    data = {
        "id": 1,
        "track_team_id": 1,
        "timeline_id": 2,
        "result_value": "Success",
        "resolution_link": "http://example.com",
        "completed_at": now,
        "notes": "Some notes",
    }
    action_status = AcceptedTeamActionStatusSchema(**data)

    assert action_status.id == 1
    assert action_status.track_team_id == 1
    assert action_status.timeline_id == 2
    assert action_status.result_value == "Success"
    assert action_status.resolution_link == "http://example.com"
    assert action_status.completed_at == now
    assert action_status.notes == "Some notes"


def test_create_action_status_base_invalid_data():
    data = {"track_team_id": "invalid", "timeline_id": "invalid"}

    with pytest.raises(ValidationError):
        ActionStatusBase(**data)


def test_update_action_status_one_field():
    data = {"t_track_team_id": 5}
    action_status_update = ActionStatusUpdate(**data)

    assert action_status_update.t_track_team_id == 5
    assert action_status_update.t_timeline_id is None
    assert action_status_update.result_value is None

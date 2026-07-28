from copy import deepcopy

from fastapi.testclient import TestClient

from src.app import app, activities


client = TestClient(app)


ORIGINAL_ACTIVITIES = deepcopy(activities)


def reset_activities():
    activities.clear()
    activities.update(deepcopy(ORIGINAL_ACTIVITIES))


def test_unregister_participant_removes_their_signup():
    # Arrange
    reset_activities()
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Removed {email} from {activity_name}"
    assert email not in activities[activity_name]["participants"]

"""
Tests for the POST /activities/{activity_name}/unregister endpoint
Uses the AAA (Arrange-Act-Assert) pattern
"""

import pytest


class TestUnregisterFromActivity:
    """Test suite for unregistering students from activities"""

    def test_unregister_existing_participant_returns_200(self, client, sample_activity):
        """Test successful unregister returns status code 200"""
        # Arrange: Get an existing participant from the activity
        activities = client.get("/activities").json()
        activity = activities[sample_activity]
        email = activity["participants"][0]

        # Act: Make POST request to unregister
        response = client.post(
            f"/activities/{sample_activity}/unregister",
            params={"email": email}
        )

        # Assert: Verify status code is 200 and message is returned
        assert response.status_code == 200
        result = response.json()
        assert "message" in result
        assert email in result["message"]

    def test_unregister_removes_participant_from_activity(self, client, sample_activity):
        """Test that unregister successfully removes participant from activity"""
        # Arrange: Get existing participant and initial count
        activities = client.get("/activities").json()
        email = activities[sample_activity]["participants"][0]
        initial_count = len(activities[sample_activity]["participants"])

        # Act: Unregister the student
        client.post(
            f"/activities/{sample_activity}/unregister",
            params={"email": email}
        )

        # Assert: Verify participant was removed
        updated = client.get("/activities").json()
        updated_count = len(updated[sample_activity]["participants"])
        assert updated_count == initial_count - 1
        assert email not in updated[sample_activity]["participants"]

    def test_unregister_nonexistent_activity_returns_404(self, client, sample_email):
        """Test unregister from non-existent activity returns 404 error"""
        # Arrange: Use non-existent activity name
        activity_name = "Nonexistent Activity"
        email = sample_email

        # Act: Make POST request to unregister from non-existent activity
        response = client.post(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )

        # Assert: Verify status code is 404 and error detail is returned
        assert response.status_code == 404
        result = response.json()
        assert "detail" in result
        assert "not found" in result["detail"].lower()

    def test_unregister_non_participant_returns_400(self, client, sample_activity, sample_email):
        """Test unregister for non-registered student returns 400 error"""
        # Arrange: Use email that is not registered
        email = sample_email
        activities = client.get("/activities").json()
        assert email not in activities[sample_activity]["participants"]

        # Act: Try to unregister non-registered student
        response = client.post(
            f"/activities/{sample_activity}/unregister",
            params={"email": email}
        )

        # Assert: Verify status code is 400 and error detail is returned
        assert response.status_code == 400
        result = response.json()
        assert "detail" in result
        assert "not registered" in result["detail"].lower()

    def test_unregister_response_message_includes_email_and_activity(self, client, sample_activity):
        """Test that success message includes both email and activity name"""
        # Arrange: Get existing participant
        activities = client.get("/activities").json()
        email = activities[sample_activity]["participants"][0]

        # Act: Unregister the student
        response = client.post(
            f"/activities/{sample_activity}/unregister",
            params={"email": email}
        )

        # Assert: Verify response message contains expected information
        result = response.json()
        message = result["message"]
        assert email in message
        assert sample_activity in message

    def test_unregister_and_signup_same_student_succeeds(self, client, sample_activity):
        """Test that a student can re-signup after unregistering"""
        # Arrange: Get existing participant
        activities = client.get("/activities").json()
        email = activities[sample_activity]["participants"][0]

        # Act: Unregister the student
        unregister_response = client.post(
            f"/activities/{sample_activity}/unregister",
            params={"email": email}
        )

        # And then sign them back up
        signup_response = client.post(
            f"/activities/{sample_activity}/signup",
            params={"email": email}
        )

        # Assert: Both operations succeed
        assert unregister_response.status_code == 200
        assert signup_response.status_code == 200
        final_activities = client.get("/activities").json()
        assert email in final_activities[sample_activity]["participants"]

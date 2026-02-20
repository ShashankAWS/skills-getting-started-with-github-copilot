"""
Tests for the POST /activities/{activity_name}/signup endpoint
Uses the AAA (Arrange-Act-Assert) pattern
"""

import pytest


class TestSignupForActivity:
    """Test suite for signing up students to activities"""

    def test_signup_valid_student_returns_200(self, client, sample_activity, sample_email):
        """Test successful signup returns status code 200"""
        # Arrange: Prepare valid activity and email
        activity_name = sample_activity
        email = sample_email

        # Act: Make POST request to signup
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert: Verify status code is 200 and message is returned
        assert response.status_code == 200
        result = response.json()
        assert "message" in result
        assert email in result["message"]

    def test_signup_adds_participant_to_activity(self, client, sample_activity, sample_email):
        """Test that signup successfully adds participant to activity"""
        # Arrange: Get initial participant count
        activity_name = sample_activity
        email = sample_email
        initial = client.get("/activities").json()
        initial_count = len(initial[activity_name]["participants"])

        # Act: Sign up the student
        client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert: Verify participant was added
        updated = client.get("/activities").json()
        updated_count = len(updated[activity_name]["participants"])
        assert updated_count == initial_count + 1
        assert email in updated[activity_name]["participants"]

    def test_signup_nonexistent_activity_returns_404(self, client, sample_email):
        """Test signup for non-existent activity returns 404 error"""
        # Arrange: Use non-existent activity name
        activity_name = "Nonexistent Activity"
        email = sample_email

        # Act: Make POST request to signup for non-existent activity
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert: Verify status code is 404 and error detail is returned
        assert response.status_code == 404
        result = response.json()
        assert "detail" in result
        assert "not found" in result["detail"].lower()

    def test_signup_duplicate_student_returns_400(self, client, sample_activity):
        """Test signup for already registered student returns 400 error"""
        # Arrange: Get an existing participant from an activity
        activities = client.get("/activities").json()
        activity = activities[sample_activity]
        existing_email = activity["participants"][0]

        # Act: Try to sign up with existing participant
        response = client.post(
            f"/activities/{sample_activity}/signup",
            params={"email": existing_email}
        )

        # Assert: Verify status code is 400 and error detail is returned
        assert response.status_code == 400
        result = response.json()
        assert "detail" in result
        assert "already" in result["detail"].lower()

    def test_signup_response_message_includes_email_and_activity(self, client, sample_activity, another_email):
        """Test that success message includes both email and activity name"""
        # Arrange: Prepare valid credentials
        activity_name = sample_activity
        email = another_email

        # Act: Sign up the student
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert: Verify response message contains expected information
        result = response.json()
        message = result["message"]
        assert email in message
        assert activity_name in message

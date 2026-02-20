"""
Tests for the GET /activities endpoint
Uses the AAA (Arrange-Act-Assert) pattern
"""

import pytest


class TestGetActivities:
    """Test suite for retrieving all activities"""

    def test_get_activities_returns_200(self, client):
        """Test that GET /activities returns status code 200"""
        # Arrange: No special setup needed

        # Act: Make GET request to /activities
        response = client.get("/activities")

        # Assert: Verify status code is 200
        assert response.status_code == 200

    def test_get_activities_returns_all_activities(self, client):
        """Test that GET /activities returns all activities"""
        # Arrange: No special setup needed

        # Act: Make GET request and parse JSON
        response = client.get("/activities")
        activities = response.json()

        # Assert: Verify we get all 9 activities
        assert len(activities) == 9
        assert "Chess Club" in activities
        assert "Programming Class" in activities
        assert "Basketball Team" in activities

    def test_activity_has_required_fields(self, client):
        """Test that each activity has all required fields"""
        # Arrange: Expected required fields
        required_fields = {"description", "schedule", "max_participants", "participants"}

        # Act: Get activities and check first one
        response = client.get("/activities")
        activities = response.json()
        first_activity = list(activities.values())[0]

        # Assert: Verify all required fields exist
        assert all(field in first_activity for field in required_fields)

    def test_activity_participants_is_list(self, client):
        """Test that participants field is a list"""
        # Arrange: No special setup needed

        # Act: Get activities
        response = client.get("/activities")
        activities = response.json()
        first_activity = list(activities.values())[0]

        # Assert: Verify participants is a list
        assert isinstance(first_activity["participants"], list)

    def test_activity_max_participants_is_integer(self, client):
        """Test that max_participants is an integer"""
        # Arrange: No special setup needed

        # Act: Get activities
        response = client.get("/activities")
        activities = response.json()
        first_activity = list(activities.values())[0]

        # Assert: Verify max_participants is an integer
        assert isinstance(first_activity["max_participants"], int)
        assert first_activity["max_participants"] > 0

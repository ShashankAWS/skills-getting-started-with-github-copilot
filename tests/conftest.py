import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


# Store original activities state
ORIGINAL_ACTIVITIES = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Basketball Team": {
        "description": "Competitive basketball team for all skill levels",
        "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
        "max_participants": 15,
        "participants": ["alex@mergington.edu"]
    },
    "Tennis Club": {
        "description": "Learn tennis fundamentals and compete in friendly matches",
        "schedule": "Saturdays, 10:00 AM - 11:30 AM",
        "max_participants": 12,
        "participants": ["grace@mergington.edu"]
    },
    "Drama Club": {
        "description": "Act in plays and musicals, explore theatrical arts",
        "schedule": "Tuesdays and Thursdays, 4:45 PM - 6:00 PM",
        "max_participants": 25,
        "participants": ["lucas@mergington.edu", "ava@mergington.edu"]
    },
    "Art Studio": {
        "description": "Painting, drawing, and sculpture instruction",
        "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 18,
        "participants": ["isabella@mergington.edu"]
    },
    "Science Olympiad": {
        "description": "Prepare for science competitions and explore STEM topics",
        "schedule": "Fridays, 4:00 PM - 5:30 PM",
        "max_participants": 16,
        "participants": ["noah@mergington.edu", "mia@mergington.edu"]
    },
    "Debate Team": {
        "description": "Develop public speaking and argumentation skills",
        "schedule": "Mondays and Thursdays, 4:30 PM - 5:45 PM",
        "max_participants": 14,
        "participants": ["liam@mergington.edu"]
    }
}


@pytest.fixture
def client():
    """Fixture providing a TestClient for the FastAPI app with reset state"""
    # Reset activities to original state before each test
    activities.clear()
    activities.update({k: {"participants": v["participants"].copy(), **{key: val for key, val in v.items() if key != "participants"}} for k, v in ORIGINAL_ACTIVITIES.items()})
    
    return TestClient(app)


@pytest.fixture
def sample_email():
    """Fixture providing a sample email for testing"""
    return "test@mergington.edu"


@pytest.fixture
def sample_activity():
    """Fixture providing a sample activity name for testing"""
    return "Chess Club"


@pytest.fixture
def another_email():
    """Fixture providing another sample email for testing"""
    return "another@mergington.edu"

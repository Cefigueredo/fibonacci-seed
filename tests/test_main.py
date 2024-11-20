import requests  # type: ignore

BASE_URL = "http://localhost:8000"


def test_root():
    response = requests.get(f"{BASE_URL}/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


def test_get_fibonacci_seed():
    response = requests.get(f"{BASE_URL}/fibonacci-seed/")
    assert response.status_code == 200
    assert "fibonacci" in response.json()


def test_post_fibonacci_seed():
    response = requests.post(
        f"{BASE_URL}/fibonacci-seed/",
        json={"datetime": "2024-11-20T09:49:08.750251"},
    )
    correct_response = {"fibonacci": "390,241,149,92,57,35,22,13,9,4"}
    assert response.status_code == 200
    assert "fibonacci" in response.json()
    assert response.json() == correct_response

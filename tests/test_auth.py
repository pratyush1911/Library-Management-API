import unittest

from fastapi.testclient import TestClient

from database import Base, engine
from main import app


class AuthTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)

    def setUp(self):
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)
        self.client = TestClient(app)

    def tearDown(self):
        self.client.close()
        engine.dispose()

    def test_signup_creates_user_and_login_works(self):
        signup_response = self.client.post(
            "/signup",
            json={"username": "alice", "password": "secret123"},
        )

        self.assertEqual(signup_response.status_code, 200)
        self.assertEqual(signup_response.json()["message"], "User created successfully")

        login_response = self.client.post(
            "/login",
            json={"username": "alice", "password": "secret123"},
        )

        self.assertEqual(login_response.status_code, 200)
        self.assertIn("access_token", login_response.json())


if __name__ == "__main__":
    unittest.main()

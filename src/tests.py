import unittest
from main import Main
import os
from faker import Faker

SERVER = os.environ.get("SERVER_URI", "ldap://localhost:389")
USER = os.environ.get("US", "admin")
PASSWORD = os.environ.get("PASSWORD", "123456")
faker = Faker()


class MainTest(unittest.TestCase):
    def test_connection(self):
        main = Main(SERVER, USER, PASSWORD, faker)

        self.assertEqual(main.failed_conn, False)


if __name__ == "__main__":
    unittest.main()
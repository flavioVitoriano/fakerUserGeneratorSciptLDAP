from ldap3 import Server, Connection, ALL, SUBTREE
from ldap3.core.exceptions import LDAPException, LDAPBindError
from dotenv import load_dotenv
import os
from faker import Faker


load_dotenv()

# env vars
SERVER = os.environ.get("SERVER", "ldap://localhost:389")
USER = os.environ.get("ADMIN", "admin")
PASSWORD = os.environ.get("PASSWORD", "123456")
ORGANIZATION_UNIT = os.environ.get("OU", "Users")
DOMAIN = os.environ.get("DOMAIN", "techinterview")
VERBOSE = bool(int(os.environ.get("VERBOSE", "0")))
CREATE_OU = bool(int(os.environ.get("CREATE_OU", "1")))
QUANTITY = int(os.environ.get("RANDOM_USERS_QUANTITY", 1000))

# faker
faker = Faker()
used_names = set()

# classes
class RandomUser:
    name = ""
    command = ""
    attrs = {}

    def __init__(self, conn, ou, domain, faker, names):
        self.faker = faker
        self.generate_name(names)
        self.command = f"cn={self.name},ou={ou},dc=techinterview,dc=com"
        self.conn = conn
        self.attrs = {"cn": USER, "sn": "AD"}

    def generate_name(self, used_names):
        name = self.faker.name()
        while name in used_names:
            name = self.faker.name()

        self.name = name
        used_names.add(name)

    def create(self):
        try:
            response = self.conn.add(
                self.command, object_class=["inetOrgPerson"], attributes=self.attrs
            )

            if VERBOSE:
                print(self.conn.result)

            return response

        except LDAPException as e:
            response = e
            print("Error: ", e)


class Main:
    failed_conn = False

    def __init__(self, uri, user, password, faker, used_names):
        self.faker = faker
        self.used_names = used_names
        try:
            self.server = Server(uri, get_info=ALL)
            self.conn = Connection(
                self.server,
                user=f"cn={user},dc=techinterview,dc=com",
                password=password,
            )
            self.b_response = self.conn.bind()
            self.user = user

        except LDAPBindError as e:
            self.failed_conn = True
            print("Error", e)

    def create_random_user(self, ou, domain):
        user = RandomUser(self.conn, ou, domain, self.faker, self.used_names)
        user.create()
        return user

    def filter(self, domain, filter):
        base = f"dc={domain},dc=com"

        try:
            self.conn.search(
                search_base=base,
                search_filter=filter,
                search_scope=SUBTREE,
                attributes=["cn", "sn", "uid", "uidNumber"],
            )
            if VERBOSE:
                print(self.conn.result)
            results = self.conn.entries
            return results

        except LDAPException as e:
            print("Error: ", e)
            results = e

    def create_ou(self, domain, ou):
        try:
            resp = self.conn.add(
                f"ou={ou},dc={domain},dc=com",
                object_class=["organizationalUnit", "top"],
            )
            if VERBOSE:
                print(self.conn.result)

        except LDAPException as e:
            print("Error: ", e)


# main
def generate_users(main, quantity):
    print("generating users...")
    iterator = map(
        lambda x: main.create_random_user(ORGANIZATION_UNIT, DOMAIN), range(quantity)
    )
    list(iterator)
    print("Done.")


def generate_ou(main):
    print("generating ou...")
    main.create_ou(DOMAIN, ORGANIZATION_UNIT)
    print("Done.")


if __name__ == "__main__":
    main = Main(SERVER, USER, PASSWORD, faker, used_names)

    if CREATE_OU:
        generate_ou(main)

    generate_users(main, QUANTITY)

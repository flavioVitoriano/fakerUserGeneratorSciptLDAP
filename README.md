# FAKE LDAP USER GENERATOR

Script for generating random users for LDAP servers

## How to use

1. Start docker-compose ( in background )

```

docker-compose up --build -d

```

2.  Generate a local env & install dependencies

```
virtualenv env
source env/bin/activate
pip install -r requirements.txt
```

3. (not required) if necessary, edit the _.env_ file in the _src_ directory, required vars: (default values and description)

```
ADMIN=admin   						# the admin user
PASSWORD=123456   					# the admin password
SERVER=ldap://localhost:389   		# the server uri
OU=Users							# the ORGANIZATION_UNIT for store users
DOMAIN=techinterview				# the domain of server
VERBOSE=0							# if greater than zero, the script print the logs in the screen
CREATE_OU=1							# if greater than zero, the script will create the OU ORGANIZATION UNIT automatically
RANDOM_USERS_QUANTITY=1200          # the quantity of fake users to generate
```

4. run the script (with env activated)

```
python src/main.py
```

## Tests

to run the tests, use python _unittest_:

```
cd src/
python -m unittest tests
```

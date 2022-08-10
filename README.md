# TODO APP
## Installation
### Dependencies
Run the following command to install dependencies.
```
pip install -r req.txt 
```
### Database
Run the following commands to initialize and create sqlite database.
```
flask db init
flask db migrate
flask db upgrade
```
### Initial Data
Run the following command to create a user.
```
flask init
```

## Usage

### Register a user
A sample request to register a user:
```
curl --location --request POST 'http://127.0.0.1:5000/api/v1/users' \
--header 'Content-Type: application/json' \
--data-raw '{
    "username":"user2",
    "password": "1234qwer",
    "email": "user2@gmail.com"
}'
```

### login
A sample request to login:
```
curl --location --request POST 'http://127.0.0.1:5000/users/login' \
--header 'Content-Type: application/json' \
--data-raw '{
    "username":"user2",
    "password": "1234qwer"
}'
```

you will get an "access_token" which you can use to authenticate.

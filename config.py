from datetime import timedelta


DEBUG=True

# in python3: import secrets => secrets.token_hex(16)
SECRET_KEY = "e987f9e9201f07efba44b908ddd1de4a"
JWT_SECRET_KEY = "e987f9e9201f07efba44b908ddd1de4a"
# JWT_COOKIE_SECURE = False
# JWT_TOKEN_LOCATION = ["cookies"]
JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=5)
# db engin setting
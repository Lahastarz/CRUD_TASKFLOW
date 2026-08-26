from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError 
hasher = PasswordHasher()
hashed_password = hasher.hash("MyDog123")
print(hashed_password)

is_correct = hasher.verify(hashed_password, "MyDog123")
print(is_correct)

def verify_password(hashed, password_guess)->bool:
    try:
        is_correct = hasher.verify(hashed, password_guess)
        return (is_correct)
    except VerifyMismatchError:
        return False
    
print(verify_password(hashed_password, "MyDog123"))   # should print True
print(verify_password(hashed_password, "WrongGuess"))  # should print False


import jwt

payload = {"sub":"user-42"}
key = "testsecret123"
algorithm = "HS256"

token = jwt.encode(payload, key, algorithm=algorithm)
print(token)

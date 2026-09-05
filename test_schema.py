# from app.auth.schemas import RegisterRequest

# valid = RegisterRequest(email="cse.24bcsh01@silicon.ac.in", password="Hello123")
# print("Valid Case: ",valid)

# try:
#     invalid = RegisterRequest(email="notanemial",password="MyDig123")
#     print("THis should Fail Now")
# except Exception as e:
#     print("Corretly Rejected the Bad email", e)

from app.auth.schemas import RegisterRequest, LoginRequest, TokenResponse, RefreshRequest

print(RegisterRequest(email="a@b.com", password="test123"))
print(LoginRequest(email="a@b.com", password="test123"))
print(TokenResponse(access_token="abc", refresh_token="def"))
print(RefreshRequest(refresh_token="xyz"))
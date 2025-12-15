import random
from secrets import token_urlsafe

def generate_otp():
    return random.randint(111111,999999)

def generate_2fa_token():
    return token_urlsafe(64)

print(generate_2fa_token())
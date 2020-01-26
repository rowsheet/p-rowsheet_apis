import string
import random

def random_string(size=64, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def random_phone_code():
    return str(random.randint(1111,9999))

if __name__ == "__main__":
    print(random_string())
    print(random_phone_code())

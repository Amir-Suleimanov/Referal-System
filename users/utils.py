import random
import string


def generate_invite_code() -> str:
    chars = string.ascii_letters + string.digits
    invite_code = ''.join(random.choice(chars) for _ in range(6))

    return invite_code
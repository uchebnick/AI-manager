import random
import string

def gen_random_string(length):
    return ''.join(random.choice(string.ascii_letters) for _ in range(length))
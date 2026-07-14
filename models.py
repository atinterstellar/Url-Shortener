import random
import string
import alchemy as sq

def generate_short_url(long,length = 6) :
    options = string.ascii_letters + string.digits
    short = "".join(random.choice(options) for _ in range(length))
    if sq.exists(short):
        sq.add_row(long,short)
    else:
        generate_short_url(long)
    return 
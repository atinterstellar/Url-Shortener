import random
import string
import alchemy as sq

shortened = set()

def generate_short_url(long,length = 6) :
    options = string.ascii_letters + string.digits
    short = "".join(random.choice(options) for _ in range(length))
    if short not in shortened:
        sq.add_row(long,short)
        shortened.add(short)
    else:
        generate_short_url(long)
    return 
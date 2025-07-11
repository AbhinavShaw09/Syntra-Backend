import random
import string


def random_razorpay_short_url():
    suffix = "".join(random.choices(string.ascii_letters + string.digits, k=8))
    return f"https://rzp.io/rzp/{suffix}"


def generate_random_username(length=8):
    return "user_" + "".join(
        random.choices(string.ascii_lowercase + string.digits, k=length)
    )


def generate_random_password(length=12):
    chars = string.ascii_letters + string.digits + string.punctuation
    return "".join(random.choices(chars, k=length))


def generate_random_email():
    username = generate_random_username(6)
    domain = random.choice(["example.com", "test.com", "mail.com"])
    return f"{username}@{domain}"


def generate_random_phone_number():
    country_code = 91  # currently supporting only india
    return f"+{country_code}-{''.join(random.choices(string.digits, k=10))}"

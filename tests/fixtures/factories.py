from dataclasses import dataclass
from faker import Faker

fake = Faker()


@dataclass
class CheckoutUser:
    first_name: str
    last_name: str
    postal_code: str


def random_checkout_user() -> CheckoutUser:
    return CheckoutUser(
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        postal_code=fake.postcode(),
    )


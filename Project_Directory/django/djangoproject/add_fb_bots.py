import argparse
import random

import django
from django.db import transaction
from django.utils import timezone

django.setup()

from minifacebook.models import Poke, Profile, Status

BATCH_SIZE = 10000

# https://www.ssa.gov/oact/babynames/decades/century.html
FIRST_NAMES = [
    "Andrew",
    "Anthony",
    "Ashley",
    "Barbara",
    "Betty",
    "Charles",
    "Christopher",
    "Daniel",
    "David",
    "Donald",
    "Donna",
    "Elizabeth",
    "Emily",
    "James",
    "Jennifer",
    "Jessica",
    "John",
    "Joseph",
    "Joshua",
    "Karen",
    "Kimberly",
    "Linda",
    "Lisa",
    "Margaret",
    "Mark",
    "Mary",
    "Matthew",
    "Michael",
    "Michelle",
    "Nancy",
    "Patricia",
    "Paul",
    "Richard",
    "Robert",
    "Sandra",
    "Sarah",
    "Steven",
    "Susan",
    "Thomas",
    "William",
]

# https://en.wikipedia.org/wiki/List_of_most_common_surnames_in_North_America
LAST_NAMES = [
    "Adams",
    "Allen",
    "Anderson",
    "Baker",
    "Brown",
    "Clark",
    "Davis",
    "Garcia",
    "Gonzalez",
    "Green",
    "Hall",
    "Harris",
    "Hernandez",
    "Jackson",
    "Johnson",
    "Jones",
    "King",
    "Lee",
    "Lewis",
    "Lopez",
    "Martin",
    "Martinez",
    "Miller",
    "Moore",
    "Nelson",
    "Perez",
    "Robinson",
    "Rodriguez",
    "Sanchez",
    "Scott",
    "Smith",
    "Taylor",
    "Thomas",
    "Thompson",
    "Walker",
    "White",
    "Williams",
    "Wilson",
    "Wright",
    "Young",
]

ADJECTIVES = ["happy", "sad", "angry", "nervous", "disappointed", "curious"]
NOUNS = ["dogs", "cats", "apples", "cars", "technology", "politics"]


def random_profile():
    first_name = random.choice(FIRST_NAMES)
    last_name = random.choice(LAST_NAMES)
    email = f"{first_name}.{last_name}@gmail.com"
    return Profile(first_name=first_name, last_name=last_name, email=email)


def main():
    argparser = argparse.ArgumentParser(description="Add fake Facebook users")
    argparser.add_argument(
        "--time-limit",
        type=float,
        default=120,
        help="Generate data until the time limit is reached",
    )
    argparser.add_argument(
        "--max-statuses",
        type=int,
        default=4,
        help="Each new profile will post up to this many statuses",
    )
    argparser.add_argument(
        "--max-pokes",
        type=int,
        default=2,
        help="Each new profile will poke up to this many other users",
    )
    args = argparser.parse_args()

    start_time = timezone.now()
    start_count = Profile.objects.count()

    profile_ids = list(Profile.objects.values_list("id", flat=True))
    # Using a transaction will increase performance, since a commit won't be
    # issued after each operation
    with transaction.atomic():
        while (timezone.now() - start_time).total_seconds() < args.time_limit:
            new_profiles = [random_profile() for _ in range(BATCH_SIZE)]
            new_profiles = Profile.objects.bulk_create(new_profiles)
            profile_ids += [p.id for p in new_profiles]
            new_statuses = []
            new_pokes = []
            # For each new profile
            for p in new_profiles:
                # Generate random statuses
                for _ in range(random.randint(1, args.max_statuses)):
                    message = (
                        f"I'm feeling {random.choice(ADJECTIVES)} "
                        f"about {random.choice(NOUNS)}!"
                    )
                    new_statuses.append(
                        Status(
                            profile=p, message=message, date_time=timezone.now()
                        )
                    )
                # Generate random pokes
                for pokee_id in random.sample(
                    profile_ids,
                    random.randint(1, min(args.max_pokes, len(profile_ids))),
                ):
                    new_pokes.append(
                        Poke(
                            poker=p, pokee_id=pokee_id, date_time=timezone.now()
                        )
                    )
            Status.objects.bulk_create(new_statuses)
            Poke.objects.bulk_create(new_pokes)
    print(f"Added {Profile.objects.count() - start_count} fake profiles")


if __name__ == "__main__":
    main()

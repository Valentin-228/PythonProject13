import random
import string
from faker import Faker

faker = Faker()

class DataGenerator:

    @staticmethod
    def generate_random_email():
        return faker.email()

    @staticmethod
    def generate_movie_name():
        return f"{faker.word().capitalize()} {faker.word().capitalize()}"

    @staticmethod
    def generate_image_url():
        return faker.image_url()

    @staticmethod
    def generate_price(min_value=10, max_value=500):
        return round(random.uniform(min_value, max_value), 2)

    @staticmethod
    def generate_description():
        return faker.sentence(nb_words=10)

    @staticmethod
    def generate_location():
        return random.choice(["SPB", "MSK"])

    @staticmethod
    def generate_published():
        return random.choice([True, False])

    @staticmethod
    def generate_genre_id(min_id=1, max_id=10):
        return random.randint(min_id, max_id)

import uuid
class Generate:
    @staticmethod
    def generate_random_string(length):
        import random
        import string

        letters = string.ascii_letters + string.digits
        return ''.join(random.choice(letters) for i in range(length))

    @staticmethod
    def generate_random_uui():
        return str(uuid.uuid4())
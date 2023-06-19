import random
import time


class Key:
    @classmethod
    def generate(cls) -> str:
        key: str = cls.generate_id(8)
        return key

    @classmethod
    def generate_id(cls, bytes: int) -> str:
        key: str = ""
        for i in range(bytes):
            generate_number: bool = True if random.randint(0, 1) else False
            if generate_number:
                key += chr(random.randint(48, 57))
            else:
                key += chr(random.randint(97, 122))

        return key

    @classmethod
    def generate_timestamp_id(cls, bytes: int):
        key: str = cls.generate_id(bytes) + str(time.time_ns())
        return key

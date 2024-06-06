import random


class HashGenerator:
    sub_keys_path = "./constants/keys.txt"
    sbox_path = "./constants/sbox.txt"

    def __init__(self):
        pass

    def keygen():
        sub_keys = []
        for line in open(HashGenerator.sub_keys_path).readlines()[1:-1]:
            sub_keys.extend([sub_key.strip() for sub_key in line.split(",")[:-1]])
        return sub_keys

    def generate_salt(n):
        key1 = ""

        for i in range(n):
            temp = str(random.randint(0, 1))
            key1 += temp

        return key1

    def generate(plaintext, salt=None, work_factor=40):
        if salt == None:
            salt = HashGenerator.generate_salt(64)

        sub_keys = HashGenerator.keygen()


plaintext = ""

HashGenerator.generate("")

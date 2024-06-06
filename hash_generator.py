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
        salt = ""

        for i in range(n):
            temp = str(random.randint(0, 1))
            salt += temp

        return salt

    def xor(p, k, size=64):
        p = p.zfill(size)
        k = k.zfill(size)

        ans = ""
        n = len(p)
        for i in range(n):

            if p[i] == k[i]:
                ans += "0"
            else:
                ans += "1"
        return ans

    def w():
        pass

    def round_box(plaintext, key):
        left_32_bit = plaintext[:32]
        right_32_bit = plaintext[32:]
        w_output = HashGenerator.w(HashGenerator.xor(left_32_bit, key))
        temp = left_32_bit
        left_32_bit = HashGenerator.xor(right_32_bit, w_output)
        return temp + right_32_bit

    def last_round(plaintext, sub_key30, sub_key31):
        left_32_bit = plaintext[:32]
        right_32_bit = plaintext[32:]
        temp = right_32_bit
        right_32_bit = HashGenerator.xor(left_32_bit, sub_key30)
        left_32_bit = HashGenerator.xor(temp, sub_key31)
        return left_32_bit + right_32_bit

    def generate_box(plaintext, sub_keys):
        final_round = plaintext
        for i in range(32):
            final_round = HashGenerator.round_box(final_round, sub_keys[i])

        return HashGenerator.last_round(final_round, sub_keys[30], sub_keys[31])

    def generate(plaintext, salt=None, work_factor=40):
        if len(plaintext) > 64:
            print("Your plaintext longer than 64 bit!")
            return

        if salt == None:
            salt = HashGenerator.generate_salt(64)

        sub_keys = HashGenerator.keygen()

        final_hash = plaintext
        for i in range(work_factor):
            final_hash = HashGenerator.xor(
                salt, HashGenerator.generate_box(final_hash, sub_keys)
            )

        return final_hash


plaintext = ""

HashGenerator.generate("")

import binascii
import random


class Sbox:
    sbox_path = "./constants/sbox.txt"

    rows_num = 32
    cols_num = 8

    def __init__(self, table):
        self.table = table

    def mapping(self, mapping_number):
        return self.table[int(mapping_number[1:6], 2)][
            int(mapping_number[0] + mapping_number[6:8], 2)
        ]

    def generate_sbox():
        sboxes = []

        sboxes_file = open(Sbox.sbox_path, "r")
        for table in HashGenerator.chunk(sboxes_file.readlines(), Sbox.rows_num + 2):
            sboxes.append(Sbox([line.split() for line in table[1:-1]]))

        sboxes_file.close()

        return sboxes


class HashGenerator:
    sub_keys_path = "./constants/keys.txt"

    block_length = 64
    round_num = 32
    sbox_num = 4

    def __init__(self):
        pass

    def get_binary(hex_string):
        return bin(int(hex_string, 16))[2:].zfill(len(hex_string[2:]) * 4)

    def get_hex(binary_string):
        return hex(int(binary_string, 2))

    def add(p, k, size=32, mod=2**32):
        addition = int(p, 2) + int(k, 2)
        return bin(addition % mod)[2:].zfill(size)

    def xor(p, k, size=32):
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

    def chunk(text, length, size=0):
        max_size = len(text) // length
        if size == 0 or size > max_size:
            size = max_size

        ans = [text[length * i : length * i + length] for i in range(size)]

        last_index = size * length
        if size == 0 and last_index < len(text):
            ans.append(text[last_index:])

        return ans

    def padding(block):
        return block.zfill(HashGenerator.block_length)

    def keygen():
        sub_keys = []
        sub_keys_file = open(HashGenerator.sub_keys_path, "r")
        for line in sub_keys_file.readlines()[1:-1]:
            sub_keys.extend(
                [
                    HashGenerator.get_binary(sub_key.strip()[:-1])
                    for sub_key in line.split(",")[:-1]
                ]
            )

        sub_keys_file.close()

        return sub_keys

    def generate_salt(n):
        salt = ""

        for i in range(n):
            temp = str(random.randint(0, 1))
            salt += temp

        return hex(int(salt, 2))

    def w(plaintext, sboxes):
        p8 = HashGenerator.chunk(plaintext, 8)

        sboxes_outputs = []
        for i in range(HashGenerator.sbox_num):
            sboxes_outputs.append(
                HashGenerator.get_binary("0x" + sboxes[i].mapping(p8[i]))
            )

        return HashGenerator.add(
            HashGenerator.xor(
                HashGenerator.add(sboxes_outputs[0], sboxes_outputs[1]),
                sboxes_outputs[2],
            ),
            sboxes_outputs[3],
        )

    def round_box(plaintext, key, sboxes):
        left_32_bit, right_32_bit = HashGenerator.chunk(plaintext, 32)
        w_output = HashGenerator.w(HashGenerator.xor(left_32_bit, key), sboxes)
        temp = left_32_bit
        left_32_bit = HashGenerator.xor(right_32_bit, w_output)
        return left_32_bit + temp

    def last_round(plaintext, sub_key30, sub_key31):
        left_32_bit, right_32_bit = HashGenerator.chunk(plaintext, 32)
        temp = right_32_bit
        right_32_bit = HashGenerator.xor(left_32_bit, sub_key30)
        left_32_bit = HashGenerator.xor(temp, sub_key31)
        return left_32_bit + right_32_bit

    def generate_box(plaintext, sub_keys, sboxes):
        final_round = plaintext
        for i in range(HashGenerator.round_num):
            final_round = HashGenerator.round_box(final_round, sub_keys[i], sboxes)

        return HashGenerator.last_round(final_round, sub_keys[30], sub_keys[31])

    def generate(plaintext, salt=None, work_factor=8):
        plaintext = HashGenerator.padding(HashGenerator.get_binary(plaintext))
        if len(plaintext) > HashGenerator.block_length:
            print(f"Your plaintext longer than {HashGenerator.block_length} bit!")
            return

        if salt == None:
            salt = HashGenerator.generate_salt(HashGenerator.block_length)

        salt = HashGenerator.padding(HashGenerator.get_binary(salt))
        if len(salt) > HashGenerator.block_length:
            print(f"Your salt longer than {HashGenerator.block_length} bit!")
            return

        sub_keys = HashGenerator.keygen()
        sboxes = Sbox.generate_sbox()

        final_hash = plaintext
        for i in range(2**work_factor):
            final_hash = HashGenerator.xor(
                salt, HashGenerator.generate_box(final_hash, sub_keys, sboxes), 64
            )

        return HashGenerator.get_hex(final_hash)

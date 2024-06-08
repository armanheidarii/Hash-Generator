from pkg.hash_generator import HashGenerator

plaintext = "0xa0a35e8ca7710"
salt = "0xd62af4866aafe96e"
work_factor = 13

print(HashGenerator.generate(plaintext, salt=salt, work_factor=work_factor))

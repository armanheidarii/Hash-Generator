import unittest
import sys

sys.path.append(".")

from pkg.hash_generator import HashGenerator, Sbox


class Test:
    def __init__(self, plaintext, salt, work_factor, output):
        self.plaintext = plaintext
        self.salt = salt
        self.work_factor = work_factor
        self.output = output


class TestHashGenerator(unittest.TestCase):
    testcase_path = "./tests/testcase.txt"

    def setUp(self):
        self.test_cases = []
        testcase_file = open(TestHashGenerator.testcase_path, "r")
        for test in HashGenerator.chunk(testcase_file.readlines(), 8):
            plaintext = test[1].split()[1].strip()[1:-1]
            salt = test[2].split()[1].strip()[1:-1]
            work_factor = test[3].split()[1].strip()
            output = test[6].strip()[1:-1]

            self.test_cases.append(Test(plaintext, salt, int(work_factor), output))

            testcase_file.close()

    def test_testcases(self):
        for test in self.test_cases:
            self.assertEqual(
                HashGenerator.generate(test.plaintext, test.salt, test.work_factor),
                test.output,
            )

    def test_1(self):
        self.assertEqual(
            HashGenerator.generate("0x9a922eef4e0cf96b", "0x3c1fc8038385785d", 7),
            "0x604f0a1246afc7ac",
        )

    def test_2(self):
        self.assertEqual(
            HashGenerator.generate("0x662d395eca6db3b8", "0xe9f923c1f12928a1", 12),
            "0x691ca028d3903c69",
        )

    def test_3(self):
        self.assertEqual(
            HashGenerator.generate("0x8096b80bc21615dd", "0xc1f7adcaccba9283", 1),
            "0x25175da0edf248d2",
        )

    def test_4(self):
        self.assertEqual(
            HashGenerator.generate("0xa0ba35e8771c2f10", "0x39df1582a7a359fb", 0),
            "0xb39efd6b4426a57e",
        )

    def test_5(self):
        self.assertEqual(
            HashGenerator.generate("0xa0ba35e87710", "0x3b2927f943b47e1b", 0),
            "0x35265f34cd085810",
        )

    def test_6(self):
        self.assertEqual(
            HashGenerator.generate("0xa0a35e8ca7710", "0xd62af4866aafe96e", 13),
            "0x6c9ecb88c7a1f4fd",
        )

    def test_7(self):
        self.assertEqual(
            HashGenerator.generate("0xa7710", "0x59c394c357335177", 15),
            "0xeb2da3ee596c65df",
        )

    def test_8(self):
        self.assertEqual(
            HashGenerator.generate("0x111111", "0x39c6c1e33ec00e2b", 1),
            "0x5038d070d6e577b0",
        )

    def test_9(self):
        self.assertEqual(
            HashGenerator.generate("0x000000000", "0x701309b2b76e6e2d", 1),
            "0x13cac2db8d45d664",
        )

    def test_10(self):
        self.assertEqual(
            HashGenerator.generate("0xacb00420042", "0x01", 3), "0x2c9f328f708ae351"
        )

    def test_11(self):
        self.assertEqual(
            HashGenerator.generate("0x8096b80bc21615dd", "0xc1f7adcaccba9283", 3),
            "0xabfe2028bbb6586d",
        )

    def test_12(self):
        self.assertEqual(
            HashGenerator.generate("0x8096b80bc21615dd", "0xc1f7adcaccba9283", 10),
            "0x7585faec42f48457",
        )

    def test_13(self):
        self.assertEqual(
            HashGenerator.generate("0x8", "0xc1f7adcaccba9283", 1), "0xf6f5b300af1442e6"
        )

    def test_14(self):
        self.assertEqual(
            HashGenerator.generate("0x8", "0xc1f7adcaccba9283", 10),
            "0x3c00bafba1cb2227",
        )

    def test_15(self):
        self.assertEqual(HashGenerator.generate("0x8", "0xc", 0), "0x7248a8880f57c99d")

    def test_16(self):
        self.assertEqual(HashGenerator.generate("0x8", "0xc", 11), "0x5d0bfa91820b314e")


if __name__ == "__main__":
    unittest.main()

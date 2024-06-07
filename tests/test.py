import unittest
import sys

sys.path.append(".")

from hash_generator import HashGenerator, Sbox


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


if __name__ == "__main__":
    unittest.main()

import unittest
from utilities.global_var import GlobalVar


class TestGlobalVar(unittest.TestCase):
    def setUp(self):
        self.name_list = 'myList'
        self.name_str = 'myString'
        self.names = [self.name_list, self.name_str]
        self.global_list = GlobalVar(self.name_list, globals_dict=globals(), myList=[1, 2, 3])
        self.global_string = GlobalVar(self.name_str, globals_dict=globals(), myString="test")

    def test_creation(self):
        self.assertEqual(self.global_list.value, [1, 2, 3])
        self.assertEqual(self.global_string.value, "test")

    def test_set_value(self):
        self.global_list.value = [4, 5, 6]
        self.assertEqual(self.global_list.value, [4, 5, 6])
        with self.assertRaises(TypeError):
            self.global_list.value = "wrong_type"

    def test_global_update(self):
        self.global_list.value = [7, 8, 9]
        self.assertEqual(globals()['myList'], [7, 8, 9])

    def test_indexing(self):
        self.assertEqual(self.global_list[0], 1)
        self.global_list[1] = 20
        self.assertEqual(self.global_list[1], 20)
        with self.assertRaises(TypeError):
            _ = self.global_string[0]

    def test_append(self):
        self.global_list.append(4)
        self.assertEqual(self.global_list.value, [1, 2, 3, 4])
        with self.assertRaises(TypeError):
            self.global_string.append("x")

    def test_length(self):
        self.assertEqual(len(self.global_list), 3)
        self.assertEqual(len(self.global_string), 4)

    def tearDown(self):
        for name in self.names:
            if name in globals():
                del globals()[name]


if __name__ == '__main__':
    unittest.main()

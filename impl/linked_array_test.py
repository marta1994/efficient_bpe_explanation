import unittest

from linked_array import LinkedArray

class LinkedArrayItem:
    def __init__(self, index, value):
        self.index = index
        self.value = value

class TestLinkedArray(unittest.TestCase):
    
    def test_init_correctly(self):
        test_array = [0, 1, 3, 5, 6, 7, 78, 12, 4, -4, -7, 1, 2]
        arr = LinkedArray(test_array)
        
        self.assertEqual(arr.len(), len(test_array))
        for i in range(len(test_array)):
            self.assertEqual(arr.get_by_index(i), test_array[i])
            self.assertEqual(arr.get_previous_index(i), i-1 if i > 0 else None)
            self.assertEqual(arr.get_next_index(i), i+1 if i < len(test_array) - 1 else None)
            self.assertEqual(arr.get_second_next_index(i), i+2 if i < len(test_array) - 2 else None)
                
    def test_replace_pair(self):
        test_array = ['f', 'h', 'a', 'l']
        arr = LinkedArray(test_array)
        
        arr.replace_pair(1, 'Z')
        
        self.assertEqual(arr.len(), len(test_array))
        self.assertEqual(arr.get_by_index(0), 'f')
        self.assertEqual(arr.get_by_index(1), 'Z')
        with self.assertRaises(ValueError):
            arr.get_by_index(2)
        self.assertEqual(arr.get_by_index(3), 'l')
        self.assertEqual(arr.get_next_index(0), 1)
        with self.assertRaises(ValueError):
            arr.get_next_index(2)
        self.assertEqual(arr.get_next_index(1), 3)
        self.assertEqual(arr.get_second_next_index(0), 3)
        self.assertEqual(arr.get_previous_index(1), 0)
        with self.assertRaises(ValueError):
            arr.get_previous_index(2)
        self.assertEqual(arr.get_previous_index(3), 1)
        
    def test_replace_all_pairs(self):
        test_array = ['f', 'h', 'a', 'l']
        arr = LinkedArray(test_array)
        
        arr.replace_pair(1, 'Z')
        arr.replace_pair(1, 'Y')
        arr.replace_pair(0, 'X')
        
        self.assertEqual(arr.len(), len(test_array))
        self.assertEqual(arr.get_by_index(0), 'X')
        with self.assertRaises(ValueError):
            arr.get_by_index(1)
        with self.assertRaises(ValueError):
            arr.get_by_index(2)
        with self.assertRaises(ValueError):
            arr.get_by_index(3)
        self.assertEqual(arr.get_next_index(0), None)
        self.assertEqual(arr.get_previous_index(0), None)
        self.assertEqual(arr.get_second_next_index(0), None)
        
    def test_replace_last_pair(self):
        test_array = ['f', 'h', 'a', 'l']
        arr = LinkedArray(test_array)
        
        arr.replace_pair(2, 'X')
        
        self.assertEqual(arr.len(), len(test_array))
        self.assertEqual(arr.get_by_index(0), 'f')
        self.assertEqual(arr.get_by_index(1), 'h')
        self.assertEqual(arr.get_by_index(2), 'X')
        with self.assertRaises(ValueError):
            arr.get_by_index(3)
        self.assertEqual(arr.get_next_index(0), 1)
        self.assertEqual(arr.get_next_index(1), 2)
        self.assertEqual(arr.get_next_index(2), None)
        self.assertEqual(arr.get_previous_index(0), None)
        self.assertEqual(arr.get_previous_index(1), 0)
        self.assertEqual(arr.get_previous_index(2), 1)
        self.assertEqual(arr.get_second_next_index(0), 2)
        self.assertEqual(arr.get_second_next_index(1), None)
        self.assertEqual(arr.get_second_next_index(2), None)
        
    def test_replace_only_pair(self):
        test_array = ['f', 'h']
        arr = LinkedArray(test_array)
        
        arr.replace_pair(0, 'X')
        
        self.assertEqual(arr.len(), len(test_array))
        self.assertEqual(arr.get_by_index(0), 'X')
        with self.assertRaises(ValueError):
            arr.get_by_index(1)
        self.assertEqual(arr.get_next_index(0), None)
        self.assertEqual(arr.get_previous_index(0), None)
        self.assertEqual(arr.get_second_next_index(0), None)
                
                
if __name__ == '__main__':
    unittest.main()
import unittest
import random

from linked_array import LinkedArray

class LinkedArrayItem:
    def __init__(self, index, value):
        self.index = index
        self.value = value

class NaiveLinkedArray:
    def __init__(self, input):
        self.array = [LinkedArrayItem(i, input[i]) for i in input]
        
    def get_by_index(self, index):
        for item in self.array:
            if item.index == index:
                return item.value
        raise ValueError("Cound not find item by index")
    
    def get_previous_index(self, index):
        ind = next((i for i, item in enumerate(self.array) if item.index == index), -1)
        if ind == -1:
            raise ValueError("Cound not find item by index")
        if ind == 0:
            return None
        return self.array[ind-1].index
    
    def get_next_index(self, index):
        ind = next((i for i, item in enumerate(self.array) if item.index == index), -1)
        if ind == -1:
            raise ValueError("Cound not find item by index")
        if ind > len(self.array) - 2:
            return None
        return self.array[ind+1].index
    
    def get_second_next_index(self, index):
        ind = next((i for i, item in enumerate(self.array) if item.index == index), -1)
        if ind == -1:
            raise ValueError("Cound not find item by index")
        if ind > len(self.array) - 3:
            return None
        return self.array[ind+2].index
    
    def replace_pair(self, index, new_item):
        ind = next((i for i, item in enumerate(self.array) if item.index == index), -1)
        if ind == -1:
            raise ValueError("Cound not find item by index")
        self.array = self.array[:ind] + [LinkedArrayItem(index, new_item)] + self.array[ind + 2:]

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
        
    # def test_random_remplace_multiple_pairs(self):
    #     test_count = 200
    #     input_size = [2, 5]
    #     replacements_count = [1, 20]
    #     for _ in range(test_count):
    #         operations = []
    #         try:
    #             arr_len = random.randint(input_size[0], input_size[1])
    #             source_arr = list(range(0, arr_len))
    #             random.shuffle(source_arr)
    #             operations.append('source array: ' + '; '.join([str(i) for i in source_arr]))
    #             arr = LinkedArray(source_arr)
    #             check_arr = NaiveLinkedArray(source_arr)
    #             actual_repl_count = min(arr_len-1, random.randint(replacements_count[0], replacements_count[1]))
    #             next_replacement = arr_len
    #             for _ in range(actual_repl_count):
    #                 replacemenet_index = random.randint(0, len(check_arr.array) - 2)
    #                 replacement_item = check_arr.array[replacemenet_index]
    #                 operations.append('replace pair: index=' + str(replacement_item.index) + '; new value=' + str(next_replacement))
    #                 try:
    #                     arr.replace_pair(replacement_item.index, next_replacement)
    #                 except:
    #                     print(' | '.join([str(i) for i in check_arr.array]))
    #                     raise
    #                 check_arr.replace_pair(replacement_item.index, next_replacement)
    #                 self.assertEqual(arr.get_by_index(replacement_item.index), check_arr.get_by_index(replacement_item.index), 'operations:\n' + '| '.join(operations))
    #                 current_ind = 0
    #                 for i in range(len(check_arr.array)):
    #                     self.assertNotEqual(current_ind, None, 'operations:\n' + '| '.join(operations))
    #                     self.assertEqual(check_arr.array[i].value, arr.get_by_index(current_ind), 'operations:\n' + '| '.join(operations))
    #                     current_ind = arr.get_next_index(current_ind)
    #                 self.assertEqual(current_ind, None, 'operations:\n' + '| '.join(operations))
    #                 next_replacement += 1
    #         except:
    #             print('operations:\n' + '| '.join(operations))
    #             raise
                
                
if __name__ == '__main__':
    unittest.main()
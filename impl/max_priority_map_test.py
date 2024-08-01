import unittest
import random
from max_priority_map import MaxPriorityMap

class Item:
    def __init__(self, map_key, heap_key):
        self.map_key = map_key
        self.heap_key = heap_key
        
    def __eq__(self, other):
        if isinstance(other, Item):
            return self.map_key == other.map_key and self.heap_key == other.heap_key
        return False
    
    def __str__(self):
        return f'map_key: {self.map_key}; heap_key: {self.heap_key}'

class TestMaxPriorityMap(unittest.TestCase):

    def test_get_max_one_element(self):
        pm = MaxPriorityMap(lambda item: item.heap_key, lambda item: item.map_key)
        pm.push(Item('a', 3))
        
        max_el = pm.pop()
        
        self.assertEqual(max_el, Item('a', 3))
        self.assertFalse(pm.contains('a'))
        self.assertEqual(pm.len(), 0)
            
    def test_raises_errors_for_empty_map(self):
        pm = MaxPriorityMap(lambda item: item.heap_key, lambda item: item.map_key)
        
        with self.assertRaises(ValueError):
            pm.get_max()
        with self.assertRaises(ValueError):
            pm.pop()
        with self.assertRaises(ValueError):
            pm.pop()
            
    def test_raises_errors_when_pushing_the_same_key(self):
        pm = MaxPriorityMap(lambda item: item.heap_key, lambda item: item.map_key)
        pm.push(Item('a', 3))
        
        with self.assertRaises(ValueError):
            pm.push(Item('a', 56))
            
    def test_raises_errors_for_unexisting_element(self):
        pm = MaxPriorityMap(lambda item: item.heap_key, lambda item: item.map_key)
        pm.push(Item('y', 12))
        pm.pop()
        
        with self.assertRaises(ValueError):
            pm.delete_by_map_key('y')
            
    def test_delete_second_max_and_pop(self):
        pm = MaxPriorityMap(lambda item: item.heap_key, lambda item: item.map_key)
        pm.push(Item('a', 3))
        pm.push(Item('b', 7))
        pm.push(Item('c', 12))
        pm.push(Item('d', 1))
        pm.push(Item('e', 5))
        pm.push(Item('f', 9))
        
        el = pm.delete_by_map_key('f')
        max_el = pm.pop()
        second_max_el = pm.get_max()
        
        self.assertEqual(el, Item('f', 9))
        self.assertFalse(pm.contains('f'))
        self.assertEqual(max_el, Item('c', 12))
        self.assertFalse(pm.contains('c'))
        self.assertEqual(second_max_el, Item('b', 7))
        self.assertTrue(pm.contains('b'))
        self.assertEqual(pm.len(), 4)
        
    def test_heap_sort(self):
        pm = MaxPriorityMap(lambda item: item.heap_key, lambda item: item.map_key)
        pm.push(Item('a', -5))
        pm.push(Item('b', 7))
        pm.push(Item('c', 2))
        pm.push(Item('d', 0))
        pm.push(Item('e', 123))
        pm.push(Item('f', 56))
        pm.push(Item('g', -76))
        pm.push(Item('h', -8))
        
        sorted_map_keys = []
        sorted_heap_keys = []
        while pm.len() > 0:
            item = pm.pop()
            sorted_map_keys.append(item.map_key)
            sorted_heap_keys.append(item.heap_key)
        
        self.assertEqual(sorted_map_keys, ['e', 'f', 'b', 'c', 'd', 'a', 'h', 'g'])
        self.assertEqual(sorted_heap_keys, [123, 56, 7, 2, 0, -5, -8, -76])
        self.assertEqual(pm.len(), 0)
        
    def test_heap_sort_with_deleted_items(self):
        pm = MaxPriorityMap(lambda item: item.heap_key, lambda item: item.map_key)
        pm.push(Item('a', -5))
        pm.push(Item('b', 7))
        pm.push(Item('c', 2))
        pm.push(Item('d', 0))
        pm.push(Item('e', 123))
        pm.push(Item('f', 56))
        pm.push(Item('g', -76))
        pm.push(Item('h', -8))
        pm.delete_by_map_key('b')
        pm.delete_by_map_key('a')
        pm.delete_by_map_key('g')
        
        sorted_map_keys = []
        sorted_heap_keys = []
        while pm.len() > 0:
            item = pm.pop()
            sorted_map_keys.append(item.map_key)
            sorted_heap_keys.append(item.heap_key)
        
        self.assertEqual(sorted_map_keys, ['e', 'f', 'c', 'd', 'h'])
        self.assertEqual(sorted_heap_keys, [123, 56, 2, 0, -8])
        self.assertEqual(pm.len(), 0)
        
    def test_heap_sort_with_deleted_and_added_items(self):
        pm = MaxPriorityMap(lambda item: item.heap_key, lambda item: item.map_key)
        pm.push(Item('a', -5))
        pm.push(Item('b', 7))
        pm.push(Item('c', 2))
        pm.push(Item('d', 0))
        pm.push(Item('e', 123))
        pm.push(Item('f', 56))
        pm.push(Item('g', -76))
        pm.push(Item('h', -8))
        pm.delete_by_map_key('b')
        pm.delete_by_map_key('a')
        pm.delete_by_map_key('g')
        pm.push(Item('g', -76))
        pm.push(Item('b', 7))
        pm.push(Item('a', -5))
        
        sorted_map_keys = []
        sorted_heap_keys = []
        while pm.len() > 0:
            item = pm.pop()
            sorted_map_keys.append(item.map_key)
            sorted_heap_keys.append(item.heap_key)
        
        self.assertEqual(sorted_heap_keys, [123, 56, 7, 2, 0, -5, -8, -76])
        self.assertEqual(sorted_map_keys, ['e', 'f', 'b', 'c', 'd', 'a', 'h', 'g'])
        self.assertEqual(pm.len(), 0)
        
    def test_heap_random_sort(self):
        test_count = 100
        num_operations = 30
        for _ in range(test_count):
            source_arr = list(range(0, num_operations))
            random.shuffle(source_arr)
            check_arr = []
            pm = MaxPriorityMap(lambda item: item.heap_key, lambda item: item.map_key)
            operations = []
            for j in range(num_operations):
                operation = random.randint(0, 3)
                match operation:
                    case 0: # pop
                        if pm.len() == 0:
                            continue
                        max_element_ind = max(enumerate(check_arr), key=lambda x: x[1].heap_key)[0]
                        check_arr = check_arr[:max_element_ind] + check_arr[max_element_ind+1:]
                        operations.append('pop')
                        pm.pop()
                        self.assertEqual(pm.len(), len(check_arr), 'operations:\n' + '; '.join(operations))
                    case 1: # delete_by_map_key
                        if pm.len() == 0:
                            continue
                        el_index = random.randint(0, pm.len() - 1)
                        map_key = check_arr[el_index].map_key
                        check_arr = check_arr[:el_index] + check_arr[el_index+1:]
                        operations.append('delete_by_map_key: ' + map_key)
                        pm.delete_by_map_key(map_key)
                        self.assertEqual(pm.len(), len(check_arr), 'operations:\n' + '; '.join(operations))
                    case _: # push
                        item = Item(str(source_arr[j]), source_arr[j])
                        check_arr.append(item)
                        operations.append('push: ' + str(item))
                        pm.push(item)
                        self.assertEqual(pm.len(), len(check_arr), 'operations:\n' + '; '.join(operations))
            check_arr = sorted(check_arr, key=lambda item: -item.heap_key)
            for item in check_arr:
                operations.append('pop')
                pm_item = pm.pop()
                self.assertEqual(item, pm_item, 'operations:\n' + '; '.join(operations))
            self.assertEqual(pm.len(), 0, 'operations:\n' + '; '.join(operations))
                        
                                 

if __name__ == '__main__':
    unittest.main()
class Node:
    def __init__(self, value, previous, next, index):
        self.value = value
        self.previous = previous
        self.next = next
        self.index = index

class LinkedArray:
    def __init__(self, items):
        self._array = [None for _ in range(len(items))]
        previous = None
        for i in range(len(items)):
            node = Node(items[i], previous, None, i)
            if previous is not None:
                previous.next = node
            self._array[i] = node
            previous = node
    
    def get_by_index(self, index):
        if self._array[index] == None:
            raise "No item by index"
        return self._array[index].value
    
    def get_previous_index(self, index):
        if self._array[index] == None:
            raise "No item by index"
        if self._array[index].previous == None:
            return None
        return self._array[index].previous.index
    
    def get_next_index(self, index):
        if self._array[index] == None:
            raise "No item by index"
        if self._array[index].next == None:
            return None
        return self._array[index].next.index
    
    def get_second_next_index(self, index):
        if self._array[index] == None:
            raise "No item by index"
        if self._array[index].next == None or self._array[index].next.next == None:
            return None
        return self._array[index].next.next.index
    
    def len(self):
        return len(self._array)
    
    def replace_pair(self, index, new_item):
        if index > len(self._array)-2 or self._array[index] == None or self._array[index].next == None:
            raise "Invalid index"
        self._array[index].value = new_item
        self._array[self._array[index].next.index] = None
        self._array[index].next = self._array[index].next.next
        if self._array[index].next is not None:
            self._array[index].next.previous = self._array[index]
class MaxPriorityMap:
    def __init__(self, heap_key, map_key):
        self._heap_key = heap_key
        self._map_key = map_key
        self._heap = []
        # Map of keys to indexes in the heap
        self._map = {}
    
    def get_max(self):
        if len(self._heap) == 0:
            raise ValueError("the heap is empty")
        return self._heap[0]
    
    def push(self, item):
        self._heap.append(item)
        map_key = self._map_key(item)
        if map_key in self._map:
            raise ValueError("Map key already exist")
        self._map[self._map_key(item)] = len(self._heap) - 1
        self._heapify_up(len(self._heap) - 1)
        
    def pop(self):
        if len(self._heap) == 0:
            raise ValueError("the heap is empty")
        self._swap(0, len(self._heap) - 1)
        item = self._heap.pop()
        map_key = self._map_key(item)
        self._map.pop(map_key)
        self._heapify_down(0)
        return item
    
    def contains(self, map_key):
        return map_key in self._map
    
    def len(self):
        if len(self._heap) != len(self._map):
            raise ValueError('Invalid state of the priority map')
        return len(self._heap) 
    
    def delete_by_map_key(self, map_key):
        if map_key not in self._map:
            raise ValueError("Map key does not exist")
        heap_index = self._map[map_key]
        item = self._heap[heap_index]
        self._swap(heap_index, len(self._heap) - 1)
        self._heap.pop()
        self._map.pop(map_key)
        if (heap_index < len(self._heap)):
            self._heapify_down(heap_index)
            self._heapify_up(heap_index)
        return item
    
    def _heapify_up(self, i):
        while i > 0 and self._heap_key(self._heap[i]) > self._heap_key(self._heap[self._parent(i)]):
            self._swap(i, self._parent(i))
            i = self._parent(i)
    
    def _heapify_down(self, i):
        largest = i
        left = self._left_child(i)
        right = self._right_child(i)

        if left < len(self._heap) and self._heap_key(self._heap[left]) > self._heap_key(self._heap[largest]):
            largest = left

        if right < len(self._heap) and self._heap_key(self._heap[right]) > self._heap_key(self._heap[largest]):
            largest = right

        if largest != i:
            self._swap(i, largest)
            self._heapify_down(largest)
    
    def _parent(self, i):
        return (i - 1) // 2

    def _left_child(self, i):
        return 2 * i + 1

    def _right_child(self, i):
        return 2 * i + 2
    
    def _swap(self, i, j):
        self._map[self._map_key(self._heap[i])] = j
        self._map[self._map_key(self._heap[j])] = i
        self._heap[i], self._heap[j] = self._heap[j], self._heap[i]
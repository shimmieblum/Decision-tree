import math


class MinHeap():
    def __init__(self) -> None:
        self.tree_array = []
        self.heap_size = 0
    
    def insert(self, key, value):
        self.tree_array.append(HeapNode(key, value))
        self.__bubble_up()
        self.heap_size += 1
        
        
    def __bubble_up(self):
        ''' traverse tree and bubble up the last value to maintain the heap property '''
        i = self.heap_size
        parent = (i-1) // 2
        while parent >= 0:
            if self.tree_array[i] < self.tree_array[parent]:
                # swap parent and child
                self.tree_array[i], self.tree_array[parent] = self.tree_array[parent], self.tree_array[i]
                i = parent
                parent = (i-1) // 2
            else: break
            
    def delete_min(self) -> 'HeapNode':
        node = self.tree_array[0]
        self.heap_size -=1
        if self.heap_size == 0: self.tree_array.pop(0)
        else: self.tree_array[0] = self.tree_array.pop(self.heap_size-1)
        self.__bubble_down()
        return node
    
    def is_empty(self):
        return self.heap_size == 0
        
    def __bubble_down(self):
        i = 0
        children = [(i * 2 )+ x for x in [1,2] if ( i* 2 ) + x  < self.heap_size]
        while children != []: 
            # print(f'parent: {i}')
            swap_child = min(children, key=lambda c: self.tree_array[c])
            # print(f'swap child {swap_child}' )
            if self.tree_array[i] > self.tree_array[swap_child]:
                self.tree_array[i], self.tree_array[swap_child] = self.tree_array[swap_child], self.tree_array[i]
                children = [(swap_child * 2 )+ x for x in [1,2] if (swap_child * 2 ) + x  < self.heap_size] 
                i = swap_child
            else: break
            
    def peek_min(self):
        if self.heap_size == 0: return None
        else: return self.tree_array[0]
            
    def print(self):
        depth = math.ceil(math.log2(1 + self.heap_size))
        
        width = 4 * (2**(depth-1))
        generation = [0]
        next_gen = []
        d = 0 
        while generation != []:
            d +=1
            s =''
            for i in generation:
                if d != depth: s = s + ' ' + str(self.tree_array[i]).center(math.ceil(width/len(generation)),' ')
                else: s = s + ' ' + str(self.tree_array[i]).center(4,' ')
                l, r = (i*2) + 1 , (i*2) + 2
                if l < self.heap_size: next_gen.append(l)
                if r < self.heap_size: next_gen.append(r)
            generation = next_gen
            next_gen = []
            # if d != depth: print(s.center(width, ' '))
            print(s)
            
    



class HeapNode():
    def __init__(self, key, value) -> None:
        self.key = key
        self.value = value
        
    def get(self):
        ''' returns the key value pair '''
        return self.key, self.value 
        
    ' === allow comparison between nodes === '
    
    def __eq__(self, other):
        if not isinstance (other, HeapNode): return False
        else: return self.key == other.key
        
    def __ne__(self, other):
        if not isinstance (other, HeapNode): return False
        else: return self.key != other.key
        
    def __lt__(self, other):
        if not isinstance (other, HeapNode): return False
        else: return self.key < other.key
        
    def __gt__(self, other):
        if not isinstance (other, HeapNode): return False
        else: return self.key > other.key
        
    
    def __lte__(self, other):
        if not isinstance (other, HeapNode): return False
        else: return self.key <= other.key
        
    def __gte__(self, other):
        if not isinstance (other, HeapNode): return False
        else: return self.key >= other.key
        
    def __str__(self) -> str:
        return f'{self.key}'
    
    def __repr__(self) -> str:
        return str(self)
    
        
    
        
    
        
            
if __name__ == '__main__':
    heap = MinHeap()
    heap.insert(1,4)
    heap.insert(2,5)
    heap.insert(10,1)
    heap.insert(10,1)
    heap.insert(10,1)
    heap.insert(5,3)
    heap.insert(5,3)
    heap.insert(5,3)
    heap.insert(5,3)
    heap.insert(2,2)
    heap.insert(2,2)
    heap.insert(2,2)
    heap.insert(2,2)
    heap.insert(2,2)
    heap.insert(2,2)
    heap.insert(2,2)
    heap.insert(2,2)
    heap.insert(2,2)
    heap.insert(2,2)
    heap.insert(10,1)
    heap.insert(10,1)
    heap.insert(10,1)
    heap.insert(10,1)
    heap.insert(10,1)
    heap.insert(10,1)
    heap.insert(10,1)
    heap.insert(10,1)
    heap.insert(10,1)
    heap.insert(10,1)
    heap.insert(10,1)
    
    
    heap.print()
    print(f'return {heap.delete_min()}')
    heap.print()
    



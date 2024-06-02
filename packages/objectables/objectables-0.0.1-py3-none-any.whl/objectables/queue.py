from collections import deque

# Strategies is incomplete and should take into account resources: ex. PostgreSQL, ASIC, etc.
class Queue(deque):
    queueing_strategies: list[str] = ('FIFO', 'LIFO')
    capacity_strategies: list[str] = ('raise exception', 'lru')
    
    def __init__(self, iterable=[], max_capacity: int = 100, queueing_strategy: str = 'FIFO', capacity_strategy: str = 'raise exception'):
        if queueing_strategy not in self.queueing_strategies or capacity_strategy not in self.capacity_strategies:
            raise Exception('Can\'t handle your strategies!')
        
        self.q_strategy = queueing_strategy
        self.c_strategy = capacity_strategy
        self.max_capacity = max_capacity
        self.count = 0
        
        deque.__init__(self, iterable, self.max_capacity)
        
    def enqueue(self, item) -> bool:
        try:
            match self.strategy:
                case 'FIFO':
                    super().appendleft(item)
                case _:
                    super().append(item)
            self.count += 1
        except:
            if self.c_strategy:
                match self.strategy:
                    case 'FIFO':
                        super().pop()
                        super().appendleft(item)
                    case _:
                        super().popleft()
                        super().append(item)
                        
                return True
            return False
        return True
    
    def dequeue(self):
        try:
            self.count = max(0, self.count - 1)
            return super().pop()
        except IndexError:
            raise IndexError("dequeue from an empty queue") from None
            
    def front(self):
        if self.count:
            return super()[-1]
        return False
    
    def rear(self):
        if self.count:
            return super()[0]
        return False
    
    def is_empty(self):
        return self.count == 0
    
    def is_full(self):
        return self.count == self.max_capacity
        
class BitQueue(deque):
    def __init__(self, number: int):
        if not isinstance(number, int):
            raise Exception(f'Only handling integers, not { type(number) }')
        
        bin_str = bin(number)[2:]
        self.count = bin_str.count('1')
        
        # Setting a max of 100
        deque.__init__(self, [x for x in bin_str], 100)
        
    def add(self, number: int, left: bool = True) -> bool:
        if number not in (0, 1):
            # raise Exception(f'Can\'t handle {number}')
            return False
        
        number = str(number)
        
        if number == '1':
            self.count += 1
            
        if left:
            super().appendleft(number)
        else:
            super().append(number)
            
        return True
            
    def pop(self, left: bool = True) -> int | bool:
        try:
            if left:
                val = super().popleft()
            else:
                val = super().pop()
                
            if val == '1':
                self.count -= 1
                
            return int(val)
        except:
            return False
    
    # Fast multiplication if maintained
    def get_val(self):
        pass
        
if __name__ == "__main__":
    # Test later!!!
    pass

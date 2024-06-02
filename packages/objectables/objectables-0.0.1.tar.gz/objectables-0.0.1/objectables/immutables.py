from collections import UserDict
from datetime import datetime

"""
# Need Cache from secret-utils 
class ImmutableCache(UserDict):
    def __init__(self, initial: dict):
        self.cache = Cache() #encryption_key=encryption_key)
        self.data = initial
        
        for key, value in initial.items():
            self.cache.add(key, value)
     
    # Function to stop deletion
    # from dictionary
    def __delitem__(self):
        raise RuntimeError("Deletion not allowed")
         
    # Function to stop pop from 
    # dictionary
    def pop(self, s = None):
        raise RuntimeError("Deletion not allowed")
         
    # Function to stop popitem 
    # from Dictionary
    def popitem(self, s = None):
        raise RuntimeError("Deletion not allowed")
        
    def __setitem__(self, key: Union[str, int, float, bytes], value: Union[str, int, float, bytes]):
        self.cache.add(key, value)
        self.data[key] = value
        
    def __str__(self):
        result = ''
        
        for idx, key in enumerate(self.keys):
            result += self.cache.get(key)
            
            if idx != (len(self.keys) - 1):
                result += ','
        
        return result
"""

class ImmutableCustomStr(str):
    pattern = "%Y-%m-%d %H:%M:%S"
    
    def __init__(self, data):
        if isinstance(data, str):
            self.type, self.data = 'str', data
        elif isinstance(data, datetime):
            self.type, self.data = 'datetime', data.strftime(self.pattern)
        else:
            raise Exception(f'Not working with this type: { type(data) }')
                
    def get(self):
        # Only two types right now!
        match self.type:
            case 'str':
                return self.data
            case _:
                # Datetime Object
                return datetime.strptime(self.data, self.pattern)
            
    def __setitem__(self, index, value):
        raise Exception('Setting is not allowed')
        
    def __delitem__(self, index):
        raise Exception('Deletion is not allowed')
        
    def __del__(self):
        return "Out of scope still works"
        
if __name__ == "__main__":
    now_obj = datetime.now()
    now_str = now_obj.strftime(ImmutableCustomStr.pattern)

    print(f'Type of now_obj is { type(now_obj) } and the type of now_str is { type(now_str)} ')

    immutable_obj = ImmutableCustomStr(now_obj)
    immutable_str = ImmutableCustomStr(now_str)

    print(f'Type of immutable_obj is { type(immutable_obj.get()) } and the type of immutable_str is { type(immutable_str.get())} ')

    try:
        immutable_obj[0] = '1'
    except Exception as e:
        print(e)
        
    try:
        del immutable_obj[0]
    except Exception as e:
        print(e)

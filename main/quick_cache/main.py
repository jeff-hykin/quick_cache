# todo
# - save to file
# - global config
#     - where to save files
#     - max in-ram size
from super_hash import super_hash

cache = {}
class FunctionCache:
    outputs = {}
    file_name: str
    def __init__(self, function):
        self.refresh = None
        self.file_name = function.__name__ if hasattr(function, "__name__") else str(id(function))

def quick_cache(function_being_wrapped):
    function_id = super_hash(function_being_wrapped)
    function_cache = cache[function_id] = cache.get(super_hash(function_being_wrapped), FunctionCache(function_being_wrapped))
    def wrapper(*args, **kwargs):
        argument_hash = super_hash(*args, **kwargs)
        if argument_hash in function_cache.outputs:
            return function_cache.outputs[argument_hash]
        
        function_cache.outputs[argument_hash] = function_being_wrapped(*args, **kwargs)
        # TODO: save output to file, read file when checking
        function_cache.refresh = lambda : function_being_wrapped(*args, **kwargs)
        return function_cache.outputs[argument_hash]
    
    wrapper.refresh = function_cache.refresh
    return wrapper

# use these later
# def large_pickle_load(file_path):
#     """
#     This is for loading really big python objects from pickle files
#     ~4Gb max value
#     """
#     import pickle
#     import os
#     max_bytes = 2**31 - 1
#     bytes_in = bytearray(0)
#     input_size = os.path.getsize(file_path)
#     with open(file_path, 'rb') as f_in:
#         for _ in range(0, input_size, max_bytes):
#             bytes_in += f_in.read(max_bytes)
#     return pickle.loads(bytes_in)

# def large_pickle_save(variable, file_path):
#     """
#     This is for saving really big python objects into a file
#     so that they can be loaded in later
#     ~4Gb max value
#     """
#     import pickle
#     bytes_out = pickle.dumps(variable, protocol=4)
#     max_bytes = 2**31 - 1
#     with open(file_path, 'wb') as f_out:
#         for idx in range(0, len(bytes_out), max_bytes):
#             f_out.write(bytes_out[idx:idx+max_bytes])

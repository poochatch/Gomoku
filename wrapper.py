import ctypes

print ctypes.CDLL('library.so').five([0,1,1,1,1,1,0],1)

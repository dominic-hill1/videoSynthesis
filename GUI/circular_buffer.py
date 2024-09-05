import ctypes

class CircularBuffer:
    """
    A class for a circular buffer used in shared memory to communicate variables in real time
    """
    def __init__(self, shared_mem, size):
        self.shared_mem = shared_mem
        self.size = size
        self.head = 0
        self.tail = 0
        self.full = False
        self.buffer = (ctypes.c_char * size).from_buffer(shared_mem.buf)

    def write(self, data):
        data = data.encode()
        data_len = len(data)
        if data_len > self.size:
            raise ValueError("Data is too large to fit into the buffer.")
        
        for byte in data:
            self.buffer[self.head] = byte
            self.head = (self.head + 1) % self.size
        self.head = 0
   

    def read(self, length):
        if self.is_empty():
            return b''
        
        result = bytearray()
        for _ in range(length):
            if self.is_empty():
                break
            result.append(self.buffer[self.tail])
            self.tail = (self.tail + 1) % self.size
            self.full = False
        return bytes(result)

    def is_empty(self):
        return not self.full and self.head == self.tail

    def cleanup(self):
        self.shared_mem.close()
        self.shared_mem.unlink()

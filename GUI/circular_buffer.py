import ctypes

class CircularBuffer:
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
            # if self.full:
            #     self.tail = (self.tail + 1) % self.size
            # self.full = self.head == self.tail
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

# if __name__ == "__main__":
#     shared_memory_name = "circular_buffer_memory"
#     buffer_size = 1024  # Buffer size of 1KB

#     # Create shared memory
#     shm = shared_memory.SharedMemory(name=shared_memory_name, create=True, size=buffer_size)
#     buffer = CircularBuffer(shm, buffer_size)
    
    # try:
    #     # Write data to the buffer
    #     data_to_write = b"Hello, Circular Buffer!"
    #     buffer.write(data_to_write)
        
    #     # Read data from the buffer
    #     read_data = buffer.read(len(data_to_write))
    #     print(f"Read data: {read_data.decode()}")

    # finally:
    #     buffer.cleanup()

import ctypes
import os

class ByteArray(ctypes.Structure):
    _fields_ = [("data", ctypes.POINTER(ctypes.c_char)),
                ("length", ctypes.c_size_t)]

class MetaDataEntry(ctypes.Structure):
    _fields_ = [("key", ctypes.c_char_p),
                ("value", ctypes.c_char_p)]

class MetaDataList(ctypes.Structure):
    _fields_ = [("entries", ctypes.POINTER(MetaDataEntry)),
                ("count", ctypes.c_int)]
    
    def to_dict(self):
        # 将entries转换为Python字典
        return {self.entries[i].key.decode("utf-8"): self.entries[i].value.decode("utf-8") for i in range(self.count)}


lib_path = os.path.join(os.path.dirname(__file__), 'lib', 'libmbtable_sdk_shared.so')
lib = ctypes.CDLL(lib_path)


lib.MbTableOpen.argtypes = [ctypes.c_char_p]
lib.MbTableOpen.restype = ctypes.c_void_p

lib.MbTableClose.argtypes = [ctypes.c_void_p]
lib.MbTableClose.restype = None

lib.MbTableRead.argtypes = [ctypes.c_void_p, ctypes.c_uint32]
lib.MbTableRead.restype = ctypes.POINTER(ByteArray)

lib.MbTableGetMetaData.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
lib.MbTableGetMetaData.restype = ctypes.POINTER(ByteArray)

lib.MbTableGetAllMetaData.argtypes = [ctypes.c_void_p, ctypes.POINTER(MetaDataList)]
lib.MbTableGetAllMetaData.restype = None

lib.MbTableGetEntryCount.argtypes = [ctypes.c_void_p]
lib.MbTableGetEntryCount.restype = ctypes.c_int32

lib.MbTableCreateIterator.argtypes = [ctypes.c_void_p, ctypes.c_uint32]
lib.MbTableCreateIterator.restype = ctypes.c_void_p

lib.IteratorGetRecord.argtypes = [ctypes.c_void_p]
lib.IteratorGetRecord.restype = ctypes.POINTER(ByteArray)

lib.IteratorHasNext.argtypes = [ctypes.c_void_p]
lib.IteratorHasNext.restype = ctypes.c_bool

lib.IteratorNext.argtypes = [ctypes.c_void_p]
lib.IteratorNext.restype = None

lib.IteratorDelete.argtypes = [ctypes.c_void_p]
lib.IteratorDelete.restype = None

lib.FreeByteArray.argtypes = [ctypes.POINTER(ByteArray)]
lib.FreeByteArray.restype = None

class MbTable:
    def __init__(self, path: str, max_retry=5):
        if not os.path.exists(path):
            raise Exception(f'MbTable file {path} not found')
        self.path = path
        self.max_retry = max_retry
        
    def get_handle(self):
        self.handle = lib.MbTableOpen(self.path.encode('utf-8'))
        retry = 0
        while not self.handle and retry < self.max_retry:
            retry += 1
            print('Failed to open mbtable, retrying in 5 second')
            import time
            import random
            time.sleep(random.randint(1, 5))
            self.handle = lib.MbTableOpen(self.path.encode('utf-8'))
        if not self.handle:
            raise Exception(f'Failed to open mbtable after {self.max_retry} retries')

        return self.handle

    def read(self, index):
        '''
        only use this method if you seek few non-sequential records, otherwise use iterator
        '''
        self.get_handle()
        value_bytes = lib.MbTableRead(self.handle, index).contents
        value = ctypes.string_at(value_bytes.data, value_bytes.length)
        lib.FreeByteArray(value_bytes)
        self.close()
        return value

    def get_metadata(self, metadata_key):
        self.get_handle()
        key_bytes = metadata_key.encode('utf-8')
        value_bytes = lib.MbTableGetMetaData(self.handle, key_bytes).contents
        value = ctypes.string_at(value_bytes.data, value_bytes.length)
        lib.FreeByteArray(value_bytes)
        self.close()
        return value
    
    def get_all_metadata(self):
        self.get_handle()
        meta_list = MetaDataList()
        lib.MbTableGetAllMetaData(self.handle, ctypes.byref(meta_list))
        return meta_list.to_dict()

    def get_entry_count(self):
        self.get_handle()
        count = lib.MbTableGetEntryCount(self.handle)
        self.close()
        return count

    def close(self):
        if self.handle:
            lib.MbTableClose(self.handle)
            self.handle = None

class MbTableIterator:
    def __init__(self, path, start_index=0, max_iterations=None):
        self.path = path
        self.start_index = start_index
        self.max_iterations = max_iterations
        self.current_iteration = 0
        self.iterator = None
        self.mbtable = None

    def __enter__(self):
        self.mbtable = MbTable(self.path)
        self.iterator = lib.MbTableCreateIterator(self.mbtable.get_handle(), self.start_index)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.iterator:
            lib.IteratorDelete(self.iterator)
        if self.mbtable:
            self.mbtable.close()

    def __iter__(self):
        return self

    def __next__(self):
        if self.max_iterations is not None and self.current_iteration >= self.max_iterations:
            raise StopIteration
        if lib.IteratorHasNext(self.iterator):
            self.current_iteration += 1
            value = self.get_record()
            lib.IteratorNext(self.iterator)
            return value
        else:
            raise StopIteration

    def next(self):
        # Python 2的兼容性方法
        return self.__next__()
    
    def get_record(self):
        ret = lib.IteratorGetRecord(self.iterator).contents
        record = ctypes.string_at(ret.data, ret.length)
        lib.FreeByteArray(ret)
        return record


if __name__ == '__main__':
    mbt_path = '/mnt/jfs-ee/jeeves-agi/projects/8691-qwen-megatron-sft-sst/checkpoints/sstable/whoru'
    mbtable = MbTable(mbt_path)
    print(mbtable.get_entry_count())
    # print(mbtable.read(1))
    print(mbtable.get_metadata('meta_key'))
    print(mbtable.get_all_metadata())
    from modelbest_sdk.dataset.thrift_wrapper.base_doc import BaseDoc
    with MbTableIterator(mbt_path) as it:
        for record in it:
            print(record)
            doc = BaseDoc.deserialize(record)
            print(doc)
            break
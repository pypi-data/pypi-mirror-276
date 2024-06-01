from collections import defaultdict
import hashlib
import numpy as np
import torch

# from modelbest_sdk.dataset.collater.collater import Collater
from modelbest_sdk.dataset.weighted_dataset import WeightedDataset
from modelbest_sdk.dataset.thrift_wrapper.base_doc import BaseDoc
from modelbest_sdk.dataset.thrift_wrapper.dataset_checkpoint import *
from modelbest_sdk.dataset.thrift_wrapper.dataset_context import DatasetContext

def default_factory_list():
    return list()

def default_factory_dict():
    return defaultdict(default_factory_list)
class BatchedDataset(torch.utils.data.IterableDataset):
    def __init__(self, context, weighted_dataset, batch_size, max_len, drop_last=False):
        self.context = context
        self.weighted_dataset = weighted_dataset
        self.max_total_length = batch_size * max_len
        self.batch_size = 1
        self.drop_last = drop_last
        
        self.buffer = []
        self.current_length = 0

        # 初始化hash_to_tag
        self.hash_to_tag = defaultdict()
      
    def put(self, data):
        self.buffer.append(data)
        self.current_length += len(data['doc'].token_ids)
    
    def pop(self):
        lengths = []
        indexes = defaultdict(default_factory_dict)        
        inputs = torch.zeros((self.batch_size, self.max_total_length), dtype=torch.int32)
        targets = torch.full((self.batch_size, self.max_total_length), dtype=torch.int32, fill_value=-100)
        dataset_ids = torch.full((self.batch_size, self.max_total_length), dtype=torch.int32, fill_value=-1)
        position_ids = torch.zeros((self.batch_size, self.max_total_length), dtype=torch.int32)
        tags = torch.full((self.batch_size, self.max_total_length), dtype=torch.int64, fill_value=-1)

        span_begin = 0
        while self.buffer:
            data = self.buffer.pop()
            chunk = data['chunk']
            index = data['index']
            dataset_idx = data['dataset_idx']
            doc: BaseDoc = data['doc']
            token_ids = doc.token_ids
            mask = doc.mask
            tag = doc.tag[0] # TODO: support multiple tags
            target_ids = np.where(mask[1:], -100, token_ids[1:]).tolist() + [-100]
            span_end = span_begin + len(token_ids)
            # TODO: what if the inputs is longer than max_total_length?
            # RuntimeError: The expanded size of the tensor (16) must match the existing size (385) at non-singleton dimension 0.  Target sizes: [16].  Tensor sizes: [385]
            inputs[0, span_begin:span_end] = torch.tensor(token_ids, dtype=torch.int32)
            targets[0, span_begin:span_end] = torch.tensor(target_ids, dtype=torch.int32)
            dataset_ids[0, span_begin:span_end] = torch.tensor(dataset_idx, dtype=torch.int32)
            position_ids[0, span_begin:span_end] = torch.from_numpy(np.arange(len(token_ids), dtype=np.int32))
            lengths.append(len(token_ids))
            indexes[int(dataset_idx)][chunk].append(index)
            tags[0, span_begin:span_end] = self.encode_tags(token_ids, tag)
            span_begin = span_end
        cu_seqlens = torch.cat(
            [torch.tensor([0] + lengths).cumsum(dim=-1), torch.tensor([self.max_total_length], dtype=torch.int32)],
            dim=0,
        ).int()
        batch = {
            "input_ids": inputs,
            "target_ids": targets,
            "dataset_ids": dataset_ids,
            "indexes": indexes,
            "cu_seqlens": cu_seqlens,
            "max_seqlen": int(torch.max(cu_seqlens[1:] - cu_seqlens[:-1])),
            "lengths": torch.tensor(sum(lengths)).int(),
            "position_ids": position_ids,
            "tags": tags,
            "hash_to_tag": self.hash_to_tag
        }
        self.current_length = 0
        return batch
        

    def will_exceed(self, data):
        return self.current_length + len(data['doc'].token_ids) > self.max_total_length

    def __iter__(self):
        for data in self.weighted_dataset:
            if self.will_exceed(data):
                yield self.pop()
            self.put(data)
        if not self.drop_last and self.buffer:
            yield self.pop()

    @staticmethod
    def collate_fn(batch):
        return batch[0]
    
    def encode_tags(self, token_ids, tag):
        tag_hash = self._get_tag_hash(tag)
        self.hash_to_tag[tag_hash] = tag
        return torch.full((len(token_ids),), tag_hash, dtype=torch.int64)
    
    def _get_tag_hash(self, tag: str) -> int:
        hash_obj = hashlib.sha256(tag.encode('utf-8'))
        return int(hash_obj.hexdigest(), 16) & ((1 << 63) - 1)

if __name__ == '__main__':
    context = DatasetContext(world_size=1, rank=0, num_workers=1)

    dataset_info_list = [
        DatasetInfo(
            path="human.BaseDoc.sstable",
            weight=1,
            max_epoch=1
        ),
        DatasetInfo(
            path="hot_chars.BaseDoc.sstable",
            weight=2,
            max_epoch=2
        )
    ]
    
    dataset_info_list = DatasetInfoList(dataset_info_list)
    
    w_dataset = WeightedDataset(
        context=context,
        dataset_info_list=dataset_info_list
    )
    
    dataset = BatchedDataset(
        context=context,
        weighted_dataset=w_dataset,
        batch_size=1,
        max_len=8192
    )
    
    for data in dataset:
        print(data)
        print(data['indexes'].keys())
        print(data['indexes'].values())
    
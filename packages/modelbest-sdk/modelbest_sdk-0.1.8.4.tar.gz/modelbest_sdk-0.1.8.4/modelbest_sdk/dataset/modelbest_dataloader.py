import os
from typing import List
from more_itertools import distribute
import torch
from modelbest_sdk.dataset.batched_dataset import BatchedDataset
from modelbest_sdk.dataset.megatron.segment_dataset import SegmentDataset
from modelbest_sdk.dataset.thrift_wrapper.dataset_checkpoint import DatasetCheckpointList, DatasetInfoList
from modelbest_sdk.dataset.thrift_wrapper.dataset_context import DatasetContext
from modelbest_sdk.dataset.weighted_dataset import WeightedDataset

class ModelbestDataloader():
    def __init__(
        self,
        context: DatasetContext,
        dataset_info_list: DatasetInfoList,
        batch_size=1,
        max_len=4096,
        prefetch_chunk_cnt=20,
        chunk_size=1024,
        num_workers=1,
        prefetch_factor=20,
        cuda_prefetch=True
    ):
        self.context = context
        self.context.num_workers = num_workers
        
        self.weighted_dataset = WeightedDataset(
            context=context, 
            dataset_info_list=dataset_info_list,
            prefetch_chunk_cnt=prefetch_chunk_cnt,
            chunk_size=chunk_size
        )
        self.setup_dataset(context, batch_size, max_len)
        
        self.dataloader = torch.utils.data.DataLoader(
            dataset=self.batched_dataset, 
            batch_size=batch_size,
            num_workers=num_workers,
            prefetch_factor=prefetch_factor,
            pin_memory=True,
            collate_fn=self.dataset_collate_fn,
        )
        
        self.cuda_prefetch = cuda_prefetch
        
        if self.cuda_prefetch:
            from modelbest_sdk.dataset.cuda_prefetcher import CudaPrefetcher
            self.cuda_prefetcher = CudaPrefetcher(
                context,
                self.dataloader
            )
        self.iterator = None

    def setup_dataset(self, context, batch_size, max_len):
        raise NotImplementedError("This method should be overridden by subclasses.")

    def dataset_collate_fn(self):
        raise NotImplementedError("This method should be overridden by subclasses.")
    
    def __iter__(self):
        if not self.cuda_prefetch:
            self.iterator = iter(self.dataloader)
        else:
            self.iterator = iter(self.cuda_prefetcher)
        return self
    
    def __next__(self):
        if self.iterator is None:
            self.__iter__()
        return next(self.iterator)
    
    def checkpoint(self):
        return self.weighted_dataset.checkpoint()
    
    def load_checkpoint(self, checkpoint):
        self.weighted_dataset.load_checkpoint(checkpoint)
        
    def update(self, dataset_entries):
        self.weighted_dataset.update(dataset_entries)
    
    def save(self, sub_dir=''):
        path = os.path.join(self.context.dataset_checkpoint_path, sub_dir, f"dataset_ckpt_rank_{self.context.rank}.mbt")
        self.checkpoint().save_to_file(path)
        
    def resume(self, sub_dir=''):
        # if dir empty, return
        resume_dir = os.path.join(self.context.dataset_checkpoint_path, sub_dir)
        if not os.path.exists(resume_dir):
            return
        if os.listdir(resume_dir) == []:
            return
        new_world_size = self.context.world_size
        first_rank_ckpt_path = os.path.join(resume_dir, f"dataset_ckpt_rank_0.mbt")
        cur_rank_ckpt_path = os.path.join(resume_dir, f"dataset_ckpt_rank_{self.context.rank}.mbt")
        old_world_size = DatasetCheckpointList.load_from_file(first_rank_ckpt_path).world_size
        if new_world_size == old_world_size:
            self.weighted_dataset.load_checkpoint(DatasetCheckpointList.load_from_file(cur_rank_ckpt_path))
        else:
            print(f"Warning: world size changed from {old_world_size} to {new_world_size}, resuming from scratch")
            merged_ckpt = None
            for path in os.listdir(resume_dir):
                abs_path = os.path.join(resume_dir, path)
                if merged_ckpt is None:
                    merged_ckpt = DatasetCheckpointList.load_from_file(abs_path)
                else:
                    merged_ckpt.merge(DatasetCheckpointList.load_from_file(abs_path))
            self.load_checkpoint(merged_ckpt)
    
    def progress(self, global_checkpoint: List[DatasetCheckpointList]):
        # This is a approximate progress calculation
        # This is used after:
        #   global_ckpt_list = [_ for _ in range(world_size)]
        #   dist.all_gather_object(global_ckpt_list, dataloader.checkpoint())
        #   dataloader.progress(global_ckpt_list)
        # or other all gather functions
        if self.context.rank != 0:
            return
        merged_ckpt = None
        for ckpt in global_checkpoint:
            if merged_ckpt is None:
                merged_ckpt = ckpt
            else:
                merged_ckpt.merge(ckpt)
        
        path_len_map = self.weighted_dataset.get_path_len_map()
        progress_dict = {}

        for checkpoint in merged_ckpt.checkpoint_list:
            dataset_info = checkpoint.dataset_info
            used = checkpoint.used
            
            total_samples_per_epoch = path_len_map[dataset_info.path]
            consumed_samples = 0
            
            
            for chunk, index_set in used.active.items():
                consumed_samples += len(index_set)
            min_epoch = 2048 if used.done else 0
            for epoch, chunk_set in used.done.items():
                min_epoch = min(min_epoch, epoch)
                for chunk in chunk_set:
                    consumed_samples += (chunk.stop - chunk.start)
            if min_epoch > 0:
                consumed_samples += total_samples_per_epoch * min_epoch

            progress_percentage = consumed_samples / total_samples_per_epoch
            
            progress_dict[dataset_info.path] = {
                "samples_per_epoch": total_samples_per_epoch,
                "samples_consumed": consumed_samples,
                "progress": progress_percentage
            }
        return progress_dict
            
class MegatronExternalDataloader(ModelbestDataloader):
    def setup_dataset(self, context, batch_size, max_len):
        self.batched_dataset = SegmentDataset(
            context=context,
            weighted_dataset=self.weighted_dataset,
            max_len=max_len
        )
        
    @staticmethod
    def dataset_collate_fn(batch):
        return SegmentDataset.collate_fn(batch)

class CpmFlashAttnDataloader(ModelbestDataloader):
    def setup_dataset(self, context, batch_size, max_len):
        self.batched_dataset = BatchedDataset(
            context=context, 
            weighted_dataset=self.weighted_dataset, 
            batch_size=batch_size, 
            max_len=max_len)
    
    @staticmethod
    def dataset_collate_fn(batch):
        return BatchedDataset.collate_fn(batch)

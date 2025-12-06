from torch.utils.data import Dataset
import os
import random
import torch
from PIL import Image
import numpy as np

try:
    import nibabel as nib
    HAS_NIBABEL = True
except ImportError:
    HAS_NIBABEL = False


class UnifiedBrainDataset(Dataset):
    def __init__(self, root_dir, transform=None, split="train", seed=42):
        assert split in ["train", "val",
                         "test"], "split must be 'train', 'val' or 'test'"
        self.root_dir = root_dir
        self.transform = transform
        self.split = split
        self.seed = seed
        self.samples = self._create_file_pairs()
        self._split_dataset()

    def _create_file_pairs(self):
        t1_dir = os.path.join(self.root_dir, "t1")
        t2_dir = os.path.join(self.root_dir, "t2")

        t1_files = set(os.listdir(t1_dir))
        t2_files = set(os.listdir(t2_dir))
        common_files = list(t1_files.intersection(t2_files))
        common_files.sort()

        pairs = [(os.path.join(t1_dir, fname), os.path.join(t2_dir, fname))
                 for fname in common_files]
        return pairs

    def _split_dataset(self):
        random.seed(self.seed)
        random.shuffle(self.samples)

        n_total = len(self.samples)
        n_train = int(n_total * 0.80)
        n_val = int(n_total * 0.05)

        if self.split == "train":
            self.samples = self.samples[:n_train]
        elif self.split == "val":
            self.samples = self.samples[n_train:n_train + n_val]
        elif self.split == "test":
            self.samples = self.samples[n_train + n_val:]

    def __len__(self):
        return len(self.samples)

    def _load_nifti_slice(self, path, slice_idx=None):
        """Load a 2D slice from a NIfTI file."""
        if not HAS_NIBABEL:
            raise ImportError("nibabel is required to load NIfTI files. Install with: pip install nibabel")
        
        nii = nib.load(path)
        data = nii.get_fdata()
        
        # Get middle slice if not specified
        if slice_idx is None:
            slice_idx = data.shape[2] // 2
        
        # Extract slice
        slice_data = data[:, :, slice_idx]
        
        # Normalize to 0-1
        slice_data = (slice_data - slice_data.min()) / (slice_data.max() - slice_data.min() + 1e-8)
        
        # Convert to PIL Image for compatibility with transforms
        slice_data = (slice_data * 255).astype(np.uint8)
        img = Image.fromarray(slice_data.T, mode='L')  # Transpose for correct orientation
        
        return img

    def __getitem__(self, idx):
        t1_path, t2_path = self.samples[idx]
        
        # Check if files are NIfTI or regular images
        if t1_path.endswith('.nii') or t1_path.endswith('.nii.gz'):
            t1_image = self._load_nifti_slice(t1_path)
            t2_image = self._load_nifti_slice(t2_path)
        else:
            t1_image = Image.open(t1_path).convert("L")
            t2_image = Image.open(t2_path).convert("L")

        if self.transform:
            t1_image = self.transform(t1_image)
            t2_image = self.transform(t2_image)

        return {
            "t1": t1_image,
            "t2": t2_image,
            "filename": os.path.basename(t1_path)
        }


class PredictionDataset(Dataset):
    def __init__(self, directory):
        super().__init__()
        self.directory = directory
        self.files = sorted([
            f for f in os.listdir(directory) if f.endswith('.pt')
        ])
        if not self.files:
            raise ValueError(f"No .pt files found in directory: {directory}")

    def __len__(self):
        return len(self.files)

    def __getitem__(self, idx):
        file_path = os.path.join(self.directory, self.files[idx])
        data = torch.load(file_path)
        # expected shape: [1, H, W] or [C, H, W]
        pred = data["prediction"]
        gt = data["target"]
        return pred, gt

#!/usr/bin/env python3
"""
Example script demonstrating how to use the IXI datasets.

This script shows how to:
1. Load the UnifiedBrainDataset
2. Create train/val/test splits
3. Visualize sample images
4. Use the dataset with a DataLoader
"""

import os
import sys
from pathlib import Path

# Add parent directory to path to import t1t2converter
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import torch
from torch.utils.data import DataLoader
from torchvision import transforms
import matplotlib.pyplot as plt

from t1t2converter.datasets import UnifiedBrainDataset


def visualize_samples(dataset, num_samples=4):
    """
    Visualize sample T1 and T2 image pairs from the dataset.
    
    Args:
        dataset: UnifiedBrainDataset instance
        num_samples: Number of samples to visualize
    """
    fig, axes = plt.subplots(2, num_samples, figsize=(15, 6))
    
    for i in range(num_samples):
        sample = dataset[i]
        t1_img = sample["t1"]
        t2_img = sample["t2"]
        filename = sample["filename"]
        
        # Convert from tensor to numpy for visualization
        if isinstance(t1_img, torch.Tensor):
            t1_img = t1_img.squeeze().numpy()
            t2_img = t2_img.squeeze().numpy()
        
        # Plot T1 image
        axes[0, i].imshow(t1_img, cmap='gray')
        axes[0, i].set_title(f"T1\n{filename}", fontsize=8)
        axes[0, i].axis('off')
        
        # Plot T2 image
        axes[1, i].imshow(t2_img, cmap='gray')
        axes[1, i].set_title(f"T2\n{filename}", fontsize=8)
        axes[1, i].axis('off')
    
    plt.tight_layout()
    plt.savefig("dataset_samples.png", dpi=150, bbox_inches='tight')
    print(f"✓ Saved visualization to dataset_samples.png")
    plt.close()


def main():
    # Configuration
    data_dir = os.environ.get("MEDICAL_I2I_DATAPATH", "./data")
    
    print("=" * 70)
    print("🧠 IXI Dataset Example")
    print("=" * 70)
    print(f"Data directory: {data_dir}")
    print()
    
    # Check if data directory exists
    if not Path(data_dir).exists():
        print(f"❌ Error: Data directory not found at {data_dir}")
        print()
        print("Please run the download script first:")
        print("  python scripts/download_datasets.py")
        sys.exit(1)
    
    # Define transforms
    transform = transforms.Compose([
        transforms.Resize((256, 256)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.5], std=[0.5])
    ])
    
    # Create datasets for each split
    print("📊 Creating datasets...")
    
    train_dataset = UnifiedBrainDataset(
        root_dir=data_dir,
        transform=transform,
        split="train",
        seed=42
    )
    
    val_dataset = UnifiedBrainDataset(
        root_dir=data_dir,
        transform=transform,
        split="val",
        seed=42
    )
    
    test_dataset = UnifiedBrainDataset(
        root_dir=data_dir,
        transform=transform,
        split="test",
        seed=42
    )
    
    print(f"✓ Train set: {len(train_dataset)} samples")
    print(f"✓ Validation set: {len(val_dataset)} samples")
    print(f"✓ Test set: {len(test_dataset)} samples")
    print(f"✓ Total: {len(train_dataset) + len(val_dataset) + len(test_dataset)} samples")
    print()
    
    # Create DataLoaders
    print("🔄 Creating DataLoaders...")
    
    train_loader = DataLoader(
        train_dataset,
        batch_size=4,
        shuffle=True,
        num_workers=2
    )
    
    val_loader = DataLoader(
        val_dataset,
        batch_size=4,
        shuffle=False,
        num_workers=2
    )
    
    test_loader = DataLoader(
        test_dataset,
        batch_size=4,
        shuffle=False,
        num_workers=2
    )
    
    print(f"✓ Train batches: {len(train_loader)}")
    print(f"✓ Validation batches: {len(val_loader)}")
    print(f"✓ Test batches: {len(test_loader)}")
    print()
    
    # Get a sample batch
    print("📦 Loading sample batch...")
    batch = next(iter(train_loader))
    
    print(f"✓ Batch T1 shape: {batch['t1'].shape}")
    print(f"✓ Batch T2 shape: {batch['t2'].shape}")
    print(f"✓ Filenames: {batch['filename'][:2]}...")  # Show first 2 filenames
    print()
    
    # Visualize samples
    print("🎨 Visualizing samples...")
    
    # Create a dataset without normalization for visualization
    viz_transform = transforms.Compose([
        transforms.Resize((256, 256)),
        transforms.ToTensor(),
    ])
    
    viz_dataset = UnifiedBrainDataset(
        root_dir=data_dir,
        transform=viz_transform,
        split="train",
        seed=42
    )
    
    visualize_samples(viz_dataset, num_samples=4)
    print()
    
    # Example training loop structure
    print("=" * 70)
    print("📝 Example Training Loop Structure")
    print("=" * 70)
    print("""
# Pseudo-code for training
for epoch in range(num_epochs):
    model.train()
    for batch in train_loader:
        t1_images = batch['t1'].to(device)
        t2_images = batch['t2'].to(device)
        
        # Forward pass
        predictions = model(t1_images)
        loss = criterion(predictions, t2_images)
        
        # Backward pass
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
    
    # Validation
    model.eval()
    with torch.no_grad():
        for batch in val_loader:
            t1_images = batch['t1'].to(device)
            t2_images = batch['t2'].to(device)
            predictions = model(t1_images)
            val_loss = criterion(predictions, t2_images)
    """)
    
    print("=" * 70)
    print("✅ Example complete!")
    print("=" * 70)
    print()
    print("Next steps:")
    print("1. Check out the training scripts in scripts/")
    print("2. Modify hyperparameters as needed")
    print("3. Run training: python scripts/unetflow_t1t2.py")
    print()


if __name__ == "__main__":
    main()


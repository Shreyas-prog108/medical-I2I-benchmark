#!/usr/bin/env python3
"""
Script to download and organize IXI datasets from Kaggle.

This script downloads two IXI datasets:
1. haonanzhou1/ixit2 - IXI T2 dataset
2. kbacon/ixi-t1 - IXI T1 dataset

The datasets are downloaded, extracted, and organized into the expected
directory structure (t1/ and t2/ folders).
"""

import os
import sys
import zipfile
import shutil
from pathlib import Path
import argparse


def setup_kaggle_credentials(kaggle_json_path):
    """
    Set up Kaggle API credentials by copying kaggle.json to ~/.kaggle/
    
    Args:
        kaggle_json_path: Path to the kaggle.json file
    """
    kaggle_dir = Path.home() / ".kaggle"
    kaggle_dir.mkdir(exist_ok=True)
    
    dest_path = kaggle_dir / "kaggle.json"
    
    if not dest_path.exists():
        shutil.copy(kaggle_json_path, dest_path)
        os.chmod(dest_path, 0o600)
        print(f"✓ Kaggle credentials copied to {dest_path}")
    else:
        print(f"✓ Kaggle credentials already exist at {dest_path}")


def download_dataset(dataset_name, download_path):
    """
    Download a Kaggle dataset.
    
    Args:
        dataset_name: Kaggle dataset identifier (e.g., 'username/dataset-name')
        download_path: Path where to download the dataset
    """
    try:
        from kaggle.api.kaggle_api_extended import KaggleApi
        
        api = KaggleApi()
        api.authenticate()
        
        print(f"\n📥 Downloading dataset: {dataset_name}")
        print(f"   Destination: {download_path}")
        
        download_path.mkdir(parents=True, exist_ok=True)
        
        api.dataset_download_files(
            dataset_name,
            path=str(download_path),
            unzip=True,
            quiet=False
        )
        
        print(f"✓ Successfully downloaded {dataset_name}")
        return True
        
    except Exception as e:
        print(f"✗ Error downloading {dataset_name}: {e}")
        return False


def organize_ixi_t1_dataset(source_dir, target_dir):
    """
    Organize IXI T1 dataset into the expected structure.
    
    Args:
        source_dir: Directory containing downloaded T1 images
        target_dir: Target directory for organized T1 images
    """
    print(f"\n📁 Organizing T1 dataset...")
    
    target_t1_dir = target_dir / "t1"
    target_t1_dir.mkdir(parents=True, exist_ok=True)
    
    # Look for image files in the source directory
    image_extensions = ['.png', '.jpg', '.jpeg', '.nii', '.nii.gz']
    
    copied_count = 0
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            if any(file.lower().endswith(ext) for ext in image_extensions):
                source_file = Path(root) / file
                target_file = target_t1_dir / file
                
                if not target_file.exists():
                    shutil.copy2(source_file, target_file)
                    copied_count += 1
    
    print(f"✓ Organized {copied_count} T1 images to {target_t1_dir}")
    return copied_count


def organize_ixi_t2_dataset(source_dir, target_dir):
    """
    Organize IXI T2 dataset into the expected structure.
    
    Args:
        source_dir: Directory containing downloaded T2 images
        target_dir: Target directory for organized T2 images
    """
    print(f"\n📁 Organizing T2 dataset...")
    
    target_t2_dir = target_dir / "t2"
    target_t2_dir.mkdir(parents=True, exist_ok=True)
    
    # Look for image files in the source directory
    image_extensions = ['.png', '.jpg', '.jpeg', '.nii', '.nii.gz']
    
    copied_count = 0
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            if any(file.lower().endswith(ext) for ext in image_extensions):
                source_file = Path(root) / file
                target_file = target_t2_dir / file
                
                if not target_file.exists():
                    shutil.copy2(source_file, target_file)
                    copied_count += 1
    
    print(f"✓ Organized {copied_count} T2 images to {target_t2_dir}")
    return copied_count


def main():
    parser = argparse.ArgumentParser(
        description="Download and organize IXI datasets from Kaggle"
    )
    parser.add_argument(
        "--data-dir",
        type=str,
        default=None,
        help="Target directory for organized datasets (default: uses MEDICAL_I2I_DATAPATH env var or ./data)"
    )
    parser.add_argument(
        "--download-dir",
        type=str,
        default="./downloads",
        help="Temporary directory for downloads (default: ./downloads)"
    )
    parser.add_argument(
        "--kaggle-json",
        type=str,
        default="./kaggle.json",
        help="Path to kaggle.json credentials file (default: ./kaggle.json)"
    )
    parser.add_argument(
        "--skip-download",
        action="store_true",
        help="Skip download step and only organize existing files"
    )
    
    args = parser.parse_args()
    
    # Determine data directory
    if args.data_dir:
        data_dir = Path(args.data_dir)
    else:
        # Try to get from environment variable or use default
        data_dir = Path(os.environ.get("MEDICAL_I2I_DATAPATH", "./data"))
    
    download_dir = Path(args.download_dir)
    kaggle_json = Path(args.kaggle_json)
    
    print("=" * 70)
    print("🧠 IXI Dataset Download and Organization Script")
    print("=" * 70)
    print(f"Data directory: {data_dir.absolute()}")
    print(f"Download directory: {download_dir.absolute()}")
    print(f"Kaggle credentials: {kaggle_json.absolute()}")
    print("=" * 70)
    
    # Check if kaggle.json exists
    if not kaggle_json.exists():
        print(f"✗ Error: Kaggle credentials file not found at {kaggle_json}")
        print("  Please ensure kaggle.json exists with your API credentials.")
        sys.exit(1)
    
    # Setup Kaggle credentials
    setup_kaggle_credentials(kaggle_json)
    
    # Dataset configurations
    datasets = [
        {
            "name": "haonanzhou1/ixit2",
            "type": "t2",
            "download_subdir": "ixit2",
        },
        {
            "name": "kbacon/ixi-t1",
            "type": "t1",
            "download_subdir": "ixi-t1",
        }
    ]
    
    # Download datasets
    if not args.skip_download:
        for dataset in datasets:
            dataset_download_path = download_dir / dataset["download_subdir"]
            success = download_dataset(dataset["name"], dataset_download_path)
            if not success:
                print(f"⚠️  Warning: Failed to download {dataset['name']}")
    else:
        print("\n⏭️  Skipping download step...")
    
    # Organize datasets
    print("\n" + "=" * 70)
    print("📂 Organizing datasets into target structure...")
    print("=" * 70)
    
    t1_count = 0
    t2_count = 0
    
    # Organize T1 dataset
    t1_source = download_dir / "ixi-t1"
    if t1_source.exists():
        t1_count = organize_ixi_t1_dataset(t1_source, data_dir)
    else:
        print(f"⚠️  Warning: T1 source directory not found at {t1_source}")
    
    # Organize T2 dataset
    t2_source = download_dir / "ixit2"
    if t2_source.exists():
        t2_count = organize_ixi_t2_dataset(t2_source, data_dir)
    else:
        print(f"⚠️  Warning: T2 source directory not found at {t2_source}")
    
    # Summary
    print("\n" + "=" * 70)
    print("✅ Dataset organization complete!")
    print("=" * 70)
    print(f"T1 images: {t1_count}")
    print(f"T2 images: {t2_count}")
    print(f"\nDataset structure:")
    print(f"  {data_dir}/")
    print(f"  ├── t1/  ({t1_count} images)")
    print(f"  └── t2/  ({t2_count} images)")
    print("=" * 70)
    
    if t1_count > 0 and t2_count > 0:
        print("\n🎉 You can now use the UnifiedBrainDataset with this data!")
        print(f"   Example: UnifiedBrainDataset(root_dir='{data_dir}')")
    else:
        print("\n⚠️  Warning: Some datasets may be missing or empty.")
        print("   Please check the download and organization steps.")


if __name__ == "__main__":
    main()


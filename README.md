# 🧠 Benchmarking GANs, Diffusion Models, and Flow Matching for T1w-to-T2w MRI Translation

This repository contains the **code and pretrained models** used in our paper:

> **Benchmarking GANs, Diffusion Models, and Flow Matching for T1w-to-T2w MRI Translation**  
> Andrea Moschetto, Lemuel Puglisi, Alec Sargood, Pierluigi Dell’Acqua, Francesco Guarnera, Sebastiano Battiato, Daniele Ravì  
> [arXiv:2507.14575](https://arxiv.org/abs/2507.14575)

---

## 🧩 Overview

Magnetic Resonance Imaging (MRI) provides different contrasts like **T1-weighted (T1w)** and **T2-weighted (T2w)** images. Acquiring both increases scan time and cost. Our work explores **image-to-image translation (I2I)** methods to synthesize T2w images from T1w inputs, potentially reducing acquisition time and cost in clinical practice.

We benchmark **three families of generative models** for this task:
- ⚔️ **Pix2Pix (GAN-based)**
- 🌫️ **Diffusion Models**
- 🌊 **Flow Matching Models**

All methods use a **shared U-Net architecture** and are trained/evaluated on three public MRI datasets (IXI, HCP, CamCAN). We provide **quantitative, qualitative, and computational comparisons**.

---

## 🚀 Getting Started


### 1. Clone the repository
```bash
git clone https://github.com/AndreaMoschetto/medical-I2I-benchmark.git
cd medical-I2I-benchmark
```

### 2. Set up environment
We recommend using [MONAI](https://monai.io) with Python 3.10 and PyTorch ≥ 1.12.
```bash
conda env create -f environment.yml
conda activate medical-i2i
```
### 3. (Optional) Install project in editable mode

If you want to use the package as a local module:

```bash
pip install -e .
```

This will make the `t1t2converter` package available for import across the project.

---

## 📂 Project Structure

```
medical-I2I-benchmark/
├── models/                   # Exported weights
├── scripts/                   # Training scripts for each model
│   ├── pix2pix_t1t2.py
│   ├── diffusion_t2.py
│   └── ...
├── src/
│   └── t1t2converter/         # Core library: models, datasets, utilities
│       ├── __init__.py
│       ├── datasets.py
│       ├── models.py
│       └── utils.py
├── .env                      # Local environment variables (not tracked)
├── .gitignore
├── environment.yml           # Conda environment definition
├── LICENSE
├── pyproject.toml            # Project/package metadata
└── README.md
```

---

## 📊 Datasets

This project uses the IXI dataset with T1 and T2-weighted MRI brain images. We provide two Kaggle datasets:

1. **IXI T2 Dataset**: [haonanzhou1/ixit2](https://www.kaggle.com/datasets/haonanzhou1/ixit2)
2. **IXI T1 Dataset**: [kbacon/ixi-t1](https://www.kaggle.com/datasets/kbacon/ixi-t1)

### Quick Start: Download Datasets

```bash
# 1. Get your Kaggle API credentials from https://www.kaggle.com/settings
# 2. Place kaggle.json in the project root
# 3. Run the download script
python scripts/download_datasets.py
```

The script will automatically:
- Download both T1 and T2 datasets from Kaggle
- Extract and organize them into the correct directory structure (`data/t1/` and `data/t2/`)
- Match corresponding T1 and T2 images by filename

For more details, see [DATASETS.md](DATASETS.md).

---

## ⚙️ Configuration

Runtime paths (like data, checkpoints, and outputs) are managed through the `utils.py` file, which reads values from environment variables. You can define your own paths by creating a `.env` file in the root directory:

```dotenv
# .env (not committed to version control)
MEDICAL_I2I_DATAPATH=/your/data/path
MEDICAL_I2I_OUTPUT=/your/output/path
MEDICAL_I2I_CKPT=/your/checkpoints/path
```

A template is provided as `.env.example`.

If not specified, default paths are created under the project directory.

---

## 🧪 Training

You can train each model independently using the corresponding script in the `scripts/` directory.  
Each script accepts command-line arguments for hyperparameters such as learning rate, batch size, number of epochs, etc.

### 🔧 Example: Train the Flow Matching model
```bash
python scripts/unetflow_t1t2.py \
    --lr 3e-4 \
    --lr_min 1e-6 \
    --batchsize 6 \
    --epochs 300 \
    --num_workers 4
```

### 📜 Common arguments

| Argument      | Default   | Description                                           |
|---------------|-----------|-------------------------------------------------------|
| `--lr`        | `3e-4`    | Initial learning rate                                |
| `--lr_min`    | `1e-6`    | Minimum LR for cosine scheduler                      |
| `--batchsize` | `6`       | Batch size                                           |
| `--epochs`    | `300`     | Total training epochs                                |
| `--num_workers` | `2`     | Number of workers for data loading                   |

> 🚨 Output checkpoints and logs will be saved under the path specified in your `.env` file (`MEDICAL_I2I_CKPT`, `MEDICAL_I2I_OUTPUT`), or fallback to defaults in `utils.py`.

---

### 🧪 Other training scripts

You can replace `unetflow_t1t2.py` with any of the following:

```bash
python scripts/pix2pix_t1t2.py
python scripts/diffusion_t2.py
python scripts/controlnet_t1t2.py
# ... etc.
```

Make sure each script supports the same CLI structure (you can check with `--help`):
```bash
python scripts/pix2pix_t1t2.py --help
```

---
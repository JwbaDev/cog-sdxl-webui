# Cog-SDXL-WEBUI Overview

The Cog-SDXL-WEBUI serves as a WEBUI for the implementation of the [SDXL](https://github.com/Stability-AI/generative-models) as a Cog model. You can find details about [Cog's packaging of machine learning models as standard containers](https://github.com/replicate/cog-sdxl) here.

<img src="images/webui.png" alt="WEBUI image" width="400"/>

## How to Use

### Generating Images

Run the following command:

```bash
cog predict -i prompt="a photo of TOK"
```

### Training the Model

1. Load the `./example_datasets/zeke.json` sample Configuration File through the WEBUI.
2. Review the configuration parameters.
3. Click the `Start training` button when ready.

## Installation Guide

### Windows

Follow this guide: [Windows Installation Guide](https://github.com/replicate/cog/blob/main/docs/wsl2/wsl2.md)

#### Steps:

1. Download and install Docker Desktop.
2. Configure WSL2.
3. Run the following commands:

```bash
sudo curl -o /usr/local/bin/cog -L "https://github.com/replicate/cog/releases/latest/download/cog_$(uname -s)_$(uname -m)"
sudo chmod +x /usr/local/bin/cog
cog run ls
git clone https://github.com/bmaltais/cog-sdxl-webui.git
cd cog-sdxl-webui
./setup.sh
```

### Linux

#### Steps:

1. Install Docker.
2. Run the following commands:

```bash
sudo curl -o /usr/local/bin/cog -L "https://github.com/replicate/cog/releases/latest/download/cog_$(uname -s)_$(uname -m)"
sudo chmod +x /usr/local/bin/cog
cog run ls
git clone https://github.com/bmaltais/cog-sdxl-webui.git
cd cog-sdxl-webui
./setup.sh
```

## Running the Cog WEBUI

To launch the webui, execute:

```bash
./webui.sh --inbrowser
```

# Training With Your Dataset

- Place 5 to 8 high-resolution images in the root of a zip file.
- Specify the zip file in the `Image file` field.
- Adjust settings as needed.
- Start the training process.

## Update Notes

### 2023-08-11

- Initial release of Minimum Viable Product for training WEBUI.
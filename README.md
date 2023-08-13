# Cog-SDXL-WEBUI Overview

The Cog-SDXL-WEBUI serves as a WEBUI for the implementation of the [SDXL](https://github.com/Stability-AI/generative-models) as a Cog model. You can find details about [Cog's packaging of machine learning models as standard containers](https://github.com/replicate/cog-sdxl) here.

<img src="images/webui.png" alt="WEBUI image" width="400"/>

## Quickstart
### Generating Images
#### ComfyUI

You can use of [ComfyUI](https://github.com/comfyanonymous/ComfyUI) with the following image for the node configuration:

<img src="images/ComfyUI_00885_.png" alt="Comfy node image" width="400"/>

Look in the training_out folder. Put the `lora.safetensors` file in the comfy lora folder and rename it to what you want. Then put the `embeddings.safetensors` file in the embedings folder, rename it to what you like. Udr them as found in the comfy image above.

### Training a quick Model

1. Load the `./example_datasets/zeke.json` sample Configuration File through the WEBUI.
2. Review the configuration parameters.
3. Click the `Start training` button when ready.

## Installation Guide

### Windows11 Native
#### Windows Pre-requirements

To install the necessary dependencies on a Windows system, follow these steps:

1. Install [Python 3.10](https://www.python.org/ftp/python/3.10.9/python-3.10.9-amd64.exe).
   - During the installation process, ensure that you select the option to add Python to the 'PATH' environment variable.

2. Install [Git](https://git-scm.com/download/win).

3. Install the [Visual Studio 2015, 2017, 2019, and 2022 redistributable](https://aka.ms/vs/17/release/vc_redist.x64.exe).
   
4. Install cuda toolkit 11.8.0

#### Steps:

1. Install cuda toolkit 11.8.0
2. Run ./setup.bat
3. Run the following commands in windows terminal:

```powershell
git clone https://github.com/bmaltais/cog-sdxl-webui.git
cd cog-sdxl-webui
.\setup.bat
.\webui.bat
```

### Windows WSL2

#### Steps:

1. Follow this guide: [Windows WSL2 Installation Guide](https://github.com/bmaltais/cog-sdxl-webui/wiki/Using-cog-on-Windows-11-with-WSL-2)
2. Run the following commands in WSL 2:

```bash
git clone https://github.com/bmaltais/cog-sdxl-webui.git
cd cog-sdxl-webui
sudo apt update -y && sudo apt install -y python3-tk 
./setup.sh
./webui.sh
```

### Linux
#### Prerequisite

Make sure to use Ubuntu 22.04 or adapt the installation to your distro

#### Steps:

1. Install Docker.
2. Install 11.8.0 cuda drivers from: https://developer.nvidia.com/cuda-toolkit-archive
3. Run the following commands:

```bash
git clone https://github.com/bmaltais/cog-sdxl-webui.git
cd cog-sdxl-webui
sudo apt update -y && sudo apt install -y python3-tk 
./setup.sh
./webui.sh
```

## Training With Your Dataset

- Place 5 to 8 high-resolution images in the root of a zip file.
- Specify the zip file in the `Image file` field.
- Adjust settings as needed.
- Start the training process.

## Update Notes

### 2023-08-13
- Convert to run without docker... much easier overall
- 
### 2023-08-11
- Initial release of Minimum Viable Product for training WEBUI.

**2021-08-12**
* Input types are inferred from input name extensions, or from the `input_images_filetype` argument
* Preprocssing are now done with fp16, and if no mask is found, the model will use the whole image

**2023-08-11**
* Default to 768x768 resolution training
* Rank as argument now, default to 32
* Now uses Swin2SR `caidas/swin2SR-realworld-sr-x4-64-bsrgan-psnr` as default, and will upscale + downscale to 768x768

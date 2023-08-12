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

### Windows

#### Steps:

1. Follow this guide: [Windows WSL2 Installation Guide](https://github.com/bmaltais/cog-sdxl-webui/wiki/Using-cog-on-Windows-11-with-WSL-2)
2. Run the following commands in WSL 2:

```bash
sudo curl -o /usr/local/bin/cog -L "https://github.com/replicate/cog/releases/latest/download/cog_$(uname -s)_$(uname -m)"
sudo chmod +x /usr/local/bin/cog
git clone https://github.com/bmaltais/cog-sdxl-webui.git
cd cog-sdxl-webui
cog run ls
```

This last command will start the docker image build process. This can take a long time. Be patient.

Finally, run the following command:

```bash
sudo apt update -y && sudo apt install -y python3-tk 
./setup.sh
```

### Linux
#### Prerequisite

Make sure to use Ubuntu 22.04 or adapt the installation to your distro

#### Steps:

1. Install Docker.
2. Install 11.8.0 cuda drivers from: https://developer.nvidia.com/cuda-toolkit-archive
3. Run the following commands:

```bash
sudo curl -o /usr/local/bin/cog -L "https://github.com/replicate/cog/releases/latest/download/cog_$(uname -s)_$(uname -m)"
sudo chmod +x /usr/local/bin/cog
git clone https://github.com/bmaltais/cog-sdxl-webui.git
cd cog-sdxl-webui
cog run ls
```

This last command will start the docker image build process. This can take a long time. Be patient.

Finally, run the following command:

```bash
sudo apt update -y && sudo apt install -y python3-tk 
./setup.sh
```

## Running the Cog WEBUI

To launch the webui, execute:

```bash
./webui.sh --inbrowser
```

## Training With Your Dataset

- Place 5 to 8 high-resolution images in the root of a zip file.
- Specify the zip file in the `Image file` field.
- Adjust settings as needed.
- Start the training process.

## Update Notes

### 2023-08-11
- Initial release of Minimum Viable Product for training WEBUI.

**2021-08-12**
* Input types are inferred from input name extensions, or from the `input_images_filetype` argument
* Preprocssing are now done with fp16, and if no mask is found, the model will use the whole image

**2023-08-11**
* Default to 768x768 resolution training
* Rank as argument now, default to 32
* Now uses Swin2SR `caidas/swin2SR-realworld-sr-x4-64-bsrgan-psnr` as default, and will upscale + downscale to 768x768

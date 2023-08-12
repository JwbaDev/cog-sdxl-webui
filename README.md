# Cog-SDXL-WEBUI

This is a WEBUI for the implementation of the [SDXL](https://github.com/Stability-AI/generative-models) as a Cog model. [Cog packages machine learning models as standard containers](https://github.com/replicate/cog).

## Basic Usage

for prediction,

```bash
cog predict -i prompt="a photo of TOK"
```

for training,

Use the WEBUI to load the `./example_datasets/zeke.json` sample Configuration File.

Look at the configuration parameters. When ready, click the `Start training` button.

## Windows Installation

You can follow this guide: https://github.com/replicate/cog/blob/main/docs/wsl2/wsl2.md

Essentially:
- Download and install Docker Desktop
- Configure WSL2

Once the above is done:

```
sudo curl -o /usr/local/bin/cog -L "https://github.com/replicate/cog/releases/latest/download/cog_$(uname -s)_$(uname -m)"
sudo chmod +x /usr/local/bin/cog
cog run ls

git clone https://github.com/bmaltais/cog-sdxl-webui.git
cd cog-sdxl-webui
./setup.sh
```

## Linux Installation

Essentially:
- Install docker

Once the above is done:

```
sudo curl -o /usr/local/bin/cog -L "https://github.com/replicate/cog/releases/latest/download/cog_$(uname -s)_$(uname -m)"
sudo chmod +x /usr/local/bin/cog
cog run ls

git clone https://github.com/bmaltais/cog-sdxl-webui.git
cd cog-sdxl-webui
./setup.sh
```

## Run the Cog WEBUI

To run the webui, simply do:

```
./webui.sh --inbrowser

```

## Update notes

- 2023-08-11
* 1st release of Minimum Viable Product for training WEBUI.
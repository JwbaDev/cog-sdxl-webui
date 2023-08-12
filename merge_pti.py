import argparse
from safetensors.torch import load_file, save_file


def main(args):
    # load embeds
    print(f"loading embeds from {args.embeds}")
    embeds = load_file(args.embeds)

    # load lora
    print(f"loading lora from {args.lora}")
    lora = load_file(args.lora)

    # copy embeds to lora state dict
    for key, value in embeds.items():
        if key == "text_encoders_0":
            key = "clip_l"
        elif key == "text_encoders_1":
            key = "clip_g"
        else:
            raise ValueError(f"unknown key {key} in embeds")

        print(f"embeds shape: {value.shape}, copying to key {key}")
        lora[key] = value

    # save lora
    print(f"saving lora to {args.output}")
    save_file(lora, args.output)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="convert PTI LoRA and embeds to single file")
    parser.add_argument("--embeds", type=str, help="embeds file")
    parser.add_argument("--lora", type=str, help="lora file")
    parser.add_argument("--output", type=str, help="output file")
    args = parser.parse_args()

    main(args)

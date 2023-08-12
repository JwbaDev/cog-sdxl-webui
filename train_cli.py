import argparse
import os
import shutil
import tarfile

from cog import BaseModel, Input, Path

from predict import SDXL_MODEL_CACHE, SDXL_URL, download_weights
from preprocess import preprocess
from trainer_pti import main as main_trainer

"""
Wrapper around actual trainer.
"""
OUTPUT_DIR = "training_out"


class TrainingOutput(BaseModel):
    weights: Path


from typing import Tuple


def train(
    input_images,
    seed,
    resolution,
    train_batch_size,
    num_train_epochs,
    max_train_steps,
    is_lora,
    unet_learning_rate,
    ti_lr,
    lora_lr,
    lora_rank,
    lr_scheduler,
    lr_warmup_steps,
    token_string,
    caption_prefix,
    mask_target_prompts,
    crop_based_on_salience,
    use_face_detection_instead,
    clipseg_temperature,
    verbose,
    checkpointing_steps,
    pivot_ratio,
    input_images_filetype,
):
    # Hard-code token_map for now. Make it configurable once we support multiple concepts or user-uploaded caption csv.
    token_map = token_string + ":2"

    # Process 'token_to_train' and 'input_data_tar_or_zip'
    inserting_list_tokens = token_map.split(",")

    token_dict = {}
    running_tok_cnt = 0
    all_token_lists = []
    for token in inserting_list_tokens:
        n_tok = int(token.split(":")[1])

        token_dict[token.split(":")[0]] = "".join(
            [f"<s{i + running_tok_cnt}>" for i in range(n_tok)]
        )
        all_token_lists.extend([f"<s{i + running_tok_cnt}>" for i in range(n_tok)])

        running_tok_cnt += n_tok

    input_dir = preprocess(
        input_images_filetype=input_images_filetype,
        input_zip_path=input_images,
        caption_text=caption_prefix,
        mask_target_prompts=mask_target_prompts,
        target_size=resolution, # update to use resolution for target size calculation
        crop_based_on_salience=crop_based_on_salience,
        use_face_detection_instead=use_face_detection_instead,
        temp=clipseg_temperature,
        substitution_tokens=list(token_dict.keys()),
    )

    if not os.path.exists(SDXL_MODEL_CACHE):
        download_weights(SDXL_URL, SDXL_MODEL_CACHE)
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
    os.makedirs(OUTPUT_DIR)

    main_trainer(
        pretrained_model_name_or_path=SDXL_MODEL_CACHE,
        instance_data_dir=os.path.join(input_dir, "captions.csv"),
        output_dir=OUTPUT_DIR,
        seed=seed,
        resolution=resolution,
        train_batch_size=train_batch_size,
        num_train_epochs=num_train_epochs,
        max_train_steps=max_train_steps,
        gradient_accumulation_steps=1,
        unet_learning_rate=unet_learning_rate,
        ti_lr=ti_lr,
        lora_lr=lora_lr,
        lr_scheduler=lr_scheduler,
        lr_warmup_steps=lr_warmup_steps,
        token_dict=token_dict,
        inserting_list_tokens=all_token_lists,
        verbose=verbose,
        checkpointing_steps=checkpointing_steps,
        scale_lr=False,
        max_grad_norm=1.0,
        allow_tf32=True,
        mixed_precision="bf16",
        device="cuda:0",
        lora_rank=lora_rank,
        is_lora=is_lora,
        pivot_ratio=pivot_ratio,
    )

    directory = Path(OUTPUT_DIR)
    out_path = "trained_model.tar"

    with tarfile.open(out_path, "w") as tar:
        for file_path in directory.rglob("*"):
            print(file_path)
            arcname = file_path.relative_to(directory)
            tar.add(file_path, arcname=arcname)

    return TrainingOutput(weights=Path(out_path))

def main():
    parser = argparse.ArgumentParser(description="Train the model with given parameters")
    parser.add_argument("--input_images", required=True, type=str, help="A .zip or .tar file containing the image files that will be used for fine-tuning")
    parser.add_argument("--seed", type=int, default=None, help="Random seed for reproducible training. Leave empty to use a random seed")
    parser.add_argument("--resolution", type=int, default=768, help="Square pixel resolution which your images will be resized to for training")
    parser.add_argument("--train_batch_size", type=int, default=4, help="Batch size (per device) for training")
    parser.add_argument("--num_train_epochs", type=int, default=4000, help="Number of epochs to loop through your training dataset")
    parser.add_argument("--max_train_steps", type=int, default=1000, help="Number of individual training steps. Takes precedence over num_train_epochs")
    parser.add_argument("--is_lora", type=bool, default=True, help="Whether to use LoRA training. If set to False, will use Full fine tuning")
    parser.add_argument("--unet_learning_rate", type=float, default=1e-6, help="Learning rate for the U-Net. We recommend this value to be somewhere between `1e-6` to `1e-5`.")
    parser.add_argument("--ti_lr", type=float, default=3e-4, help="Scaling of learning rate for training textual inversion embeddings. Don't alter unless you know what you're doing.")
    parser.add_argument("--lora_lr", type=float, default=1e-4, help="Scaling of learning rate for training LoRA embeddings. Don't alter unless you know what you're doing.")
    parser.add_argument("--lora_rank", type=int, default=32, help="Rank of LoRA embeddings. Don't alter unless you know what you're doing.")
    parser.add_argument("--lr_scheduler", type=str, choices=["constant", "linear"], default="constant", help="Learning rate scheduler to use for training")
    parser.add_argument("--lr_warmup_steps", type=int, default=100, help="Number of warmup steps for lr schedulers with warmups.")
    parser.add_argument("--token_string", type=str, default="TOK", help="A unique string that will be trained to refer to the concept in the input images. Can be anything, but TOK works well")
    parser.add_argument("--caption_prefix", type=str, default="a photo of TOK, ", help="Text which will be used as prefix during automatic captioning. Must contain the `token_string`.")
    parser.add_argument("--mask_target_prompts", type=str, default=None, help="Prompt that describes part of the image that you will find important. For example, if you are fine-tuning your pet, `photo of a dog` will be a good prompt. Prompt-based masking is used to focus the fine-tuning process on the important/salient parts of the image")
    parser.add_argument("--crop_based_on_salience", type=bool, default=True, help="If you want to crop the image to `target_size` based on the important parts of the image, set this to True. If you want to crop the image based on face detection, set this to False")
    parser.add_argument("--use_face_detection_instead", type=bool, default=False, help="If you want to use face detection instead of CLIPSeg for masking. For face applications, we recommend using this option.")
    parser.add_argument("--clipseg_temperature", type=float, default=1.0, help="How blurry you want the CLIPSeg mask to be. We recommend this value be something between `0.5` to `1.0`. If you want to have more sharp mask (but thus more errorful), you can decrease this value.")
    parser.add_argument("--verbose", type=bool, default=True, help="Verbose output")
    parser.add_argument("--checkpointing_steps", type=int, default=999999, help="Number of steps between saving checkpoints. Set to very very high number to disable checkpointing, because you don't need one.")
    parser.add_argument("--pivot_ratio", type=float, default=0.5, help="When should training should pivot from TI to LoRA/ Default is midway (0.5)")
    parser.add_argument("--input_images_filetype", type=str, choices=["zip", "tar", "infer"], default="infer", help="Filetype of the input images. Can be either `zip` or `tar`. By default its `infer`, and it will be inferred from the ext of input file.")

    args = parser.parse_args()

    train(
        input_images=args.input_images,
        seed=args.seed,
        resolution=args.resolution,
        train_batch_size=args.train_batch_size,
        num_train_epochs=args.num_train_epochs,
        max_train_steps=args.max_train_steps,
        is_lora=args.is_lora,
        unet_learning_rate=args.unet_learning_rate,
        ti_lr=args.ti_lr,
        lora_lr=args.lora_lr,
        lora_rank=args.lora_rank,
        lr_scheduler=args.lr_scheduler,
        lr_warmup_steps=args.lr_warmup_steps,
        token_string=args.token_string,
        caption_prefix=args.caption_prefix,
        mask_target_prompts=args.mask_target_prompts,
        crop_based_on_salience=args.crop_based_on_salience,
        use_face_detection_instead=args.use_face_detection_instead,
        clipseg_temperature=args.clipseg_temperature,
        verbose=args.verbose,
        checkpointing_steps=args.checkpointing_steps,
        pivot_ratio=args.pivot_ratio,
        input_images_filetype=args.input_images_filetype
    )


if __name__ == "__main__":
    main()

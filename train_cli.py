import argparse
from train import train


def main():
    parser = argparse.ArgumentParser(description="Train the model with given parameters")
    parser.add_argument("--caption_prefix", type=str, default="a photo of TOK, ", help="Text which will be used as prefix during automatic captioning. Must contain the `token_string`.")
    parser.add_argument("--checkpointing_steps", type=int, default=999999, help="Number of steps between saving checkpoints. Set to very very high number to disable checkpointing, because you don't need one.")
    parser.add_argument("--clipseg_temperature", type=float, default=1.0, help="How blurry you want the CLIPSeg mask to be. We recommend this value be something between `0.5` to `1.0`. If you want to have more sharp mask (but thus more errorful), you can decrease this value.")
    parser.add_argument("--crop_based_on_salience", action="store_true", help="If you want to crop the image to `target_size` based on the important parts of the image, set this to True. If you want to crop the image based on face detection, set this to False")
    parser.add_argument("--input_images", required=True, type=str, help="A .zip or .tar file containing the image files that will be used for fine-tuning")
    parser.add_argument("--input_images_filetype", type=str, choices=["zip", "tar", "infer"], default="infer", help="Filetype of the input images. Can be either `zip` or `tar`. By default its `infer`, and it will be inferred from the ext of input file.")
    parser.add_argument("--is_lora", action="store_true", help="Whether to use LoRA training. If set to False, will use Full fine tuning")
    parser.add_argument("--lora_lr", type=float, default=1e-4, help="Scaling of learning rate for training LoRA embeddings. Don't alter unless you know what you're doing.")
    parser.add_argument("--lora_rank", type=int, default=32, help="Rank of LoRA embeddings. Don't alter unless you know what you're doing.")
    parser.add_argument("--lr_scheduler", type=str, choices=["constant", "linear"], default="constant", help="Learning rate scheduler to use for training")
    parser.add_argument("--lr_warmup_steps", type=int, default=100, help="Number of warmup steps for lr schedulers with warmups.")
    parser.add_argument("--mask_target_prompts", type=str, default=None, help="Prompt that describes part of the image that you will find important. For example, if you are fine-tuning your pet, `photo of a dog` will be a good prompt. Prompt-based masking is used to focus the fine-tuning process on the important/salient parts of the image")
    parser.add_argument("--max_train_steps", type=int, default=1000, help="Number of individual training steps. Takes precedence over num_train_epochs")
    parser.add_argument("--num_train_epochs", type=int, default=4000, help="Number of epochs to loop through your training dataset")
    parser.add_argument("--output_lora_dir", type=str, default="constant", help="Path to LoRA directory")
    parser.add_argument("--output_embedding_dir", type=str, default="constant", help="Path to embedding directory")
    parser.add_argument("--output_name", type=str, default="constant", help="Name of the model")
    parser.add_argument("--pivot_ratio", type=float, default=0.5, help="When should training should pivot from TI to LoRA/ Default is midway (0.5)")
    parser.add_argument("--resolution", type=int, default=768, help="Square pixel resolution which your images will be resized to for training")
    parser.add_argument("--seed", type=int, default=None, help="Random seed for reproducible training. Leave empty to use a random seed")
    parser.add_argument("--ti_lr", type=float, default=3e-4, help="Scaling of learning rate for training textual inversion embeddings. Don't alter unless you know what you're doing.")
    parser.add_argument("--token_string", type=str, default="TOK", help="A unique string that will be trained to refer to the concept in the input images. Can be anything, but TOK works well")
    parser.add_argument("--train_batch_size", type=int, default=4, help="Batch size (per device) for training")
    parser.add_argument("--unet_learning_rate", type=float, default=1e-6, help="Learning rate for the U-Net. We recommend this value to be somewhere between `1e-6` to `1e-5`.")
    parser.add_argument("--use_face_detection_instead", action="store_true", help="If you want to use face detection instead of CLIPSeg for masking. For face applications, we recommend using this option.")
    parser.add_argument("--verbose", action="store_true", help="Verbose output")

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
        input_images_filetype=args.input_images_filetype,
        output_name=args.output_name,
        output_lora_dir=args.output_lora_dir,
        output_embedding_dir=args.output_embedding_dir,
    )


if __name__ == "__main__":
    main()

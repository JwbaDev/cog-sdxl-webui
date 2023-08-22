import gradio as gr
from .common_gui import remove_doublequote, get_folder_path, get_file_path, get_any_file_path

class Folders:
    def __init__(self, headless=False):
        self.headless = headless
        
        with gr.Row():
            self.input_images = gr.Textbox(
                label='Image zip file',
                placeholder='Path to zip file where the training images are located',
            )
            self.input_images_folder = gr.Button(
                '📂', elem_id='open_folder_small', visible=(not self.headless)
            )
            self.input_images_folder.click(
                get_file_path,
                outputs=self.input_images,
                show_progress=False,
            )
            self.output_name = gr.Textbox(
                label='Model output name',
                placeholder='(Name of the model to output)',
                value='last',
                interactive=True,
            )
            # self.reg_data_dir = gr.Textbox(
            #     label='Regularisation folder',
            #     placeholder='(Optional) Folder where where the regularization folders containing the images are located',
            # )
            # self.reg_data_dir_folder = gr.Button(
            #     '📂', elem_id='open_folder_small', visible=(not self.headless)
            # )
            # self.reg_data_dir_folder.click(
            #     get_folder_path,
            #     outputs=self.reg_data_dir,
            #     show_progress=False,
            # )
        with gr.Row():
            self.output_lora_dir = gr.Textbox(
                label='Output folder LoRA',
                placeholder='Folder to output the trained LoRA model',
                value='./training_out',
            )
            self.output_lora_dir_folder = gr.Button(
                '📂', elem_id='open_folder_small', visible=(not self.headless)
            )
            self.output_lora_dir_folder.click(
                get_folder_path,
                outputs=self.output_lora_dir,
                show_progress=False,
            )
            self.output_embedding_dir = gr.Textbox(
                label='Output folder embedding',
                placeholder='Folder to output the trained embedding',
                value='./training_out',
            )
            self.output_embedding_dir_folder = gr.Button(
                '📂', elem_id='open_folder_small', visible=(not self.headless)
            )
            self.output_embedding_dir_folder.click(
                get_folder_path,
                outputs=self.output_embedding_dir,
                show_progress=False,
            )
        # with gr.Row():
            
            # self.training_comment = gr.Textbox(
            #     label='Training comment',
            #     placeholder='(Optional) Add training comment to be included in metadata',
            #     interactive=True,
            # )
        self.input_images.blur(
            remove_doublequote,
            inputs=[self.input_images],
            outputs=[self.input_images],
        )
        # self.reg_data_dir.blur(
        #     remove_doublequote,
        #     inputs=[self.reg_data_dir],
        #     outputs=[self.reg_data_dir],
        # )
        self.output_lora_dir.blur(
            remove_doublequote,
            inputs=[self.output_lora_dir],
            outputs=[self.output_lora_dir],
        )
        self.output_embedding_dir.blur(
            remove_doublequote,
            inputs=[self.output_embedding_dir],
            outputs=[self.output_embedding_dir],
        )
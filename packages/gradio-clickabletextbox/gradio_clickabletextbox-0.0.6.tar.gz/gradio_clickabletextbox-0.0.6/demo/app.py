
import gradio as gr
from gradio_clickabletextbox import ClickableTextbox

prompts = ["This is a prompt", "This is another prompt", "This is a third prompt This is a third promptThis is a third promptThis is a third promptThis is a third promptThis is a third prompt This is a third prompt This is a third prompt"
           ]
suffixes = ["This is a suffix", "This is another suffix", "This is a third suffix"
            ]
demo = gr.Interface(
    lambda x: x,
    # interactive version of your component
    ClickableTextbox(suffixes=suffixes, prompts=prompts),
    ClickableTextbox(suffixes=suffixes, prompts=prompts,),
)

if __name__ == "__main__":
    demo.launch(server_port=1236)

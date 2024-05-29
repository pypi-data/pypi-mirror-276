
import gradio as gr
from app import demo as app
import os

_docs = {'ClickableTextbox': {'description': 'Creates a textarea for user to enter string input or display string output.\n', 'members': {'__init__': {'value': {'type': 'str | Callable | None', 'default': 'None', 'description': 'default text to provide in textarea. If callable, the function will be called whenever the app loads to set the initial value of the component.'}, 'lines': {'type': 'int', 'default': '1', 'description': 'minimum number of line rows to provide in textarea.'}, 'max_lines': {'type': 'int', 'default': '20', 'description': 'maximum number of line rows to provide in textarea.'}, 'placeholder': {'type': 'str | None', 'default': 'None', 'description': 'placeholder hint to provide behind textarea.'}, 'label': {'type': 'str | None', 'default': 'None', 'description': 'The label for this component. Appears above the component and is also used as the header if there are a table of examples for this component. If None and used in a `gr.Interface`, the label will be the name of the parameter this component is assigned to.'}, 'info': {'type': 'str | None', 'default': 'None', 'description': 'additional component description.'}, 'every': {'type': 'float | None', 'default': 'None', 'description': "If `value` is a callable, run the function 'every' number of seconds while the client connection is open. Has no effect otherwise. The event can be accessed (e.g. to cancel it) via this component's .load_event attribute."}, 'show_label': {'type': 'bool | None', 'default': 'None', 'description': 'if True, will display label. If False, the copy button is hidden as well as well as the label.'}, 'container': {'type': 'bool', 'default': 'True', 'description': 'If True, will place the component in a container - providing some extra padding around the border.'}, 'scale': {'type': 'int | None', 'default': 'None', 'description': 'relative size compared to adjacent Components. For example if Components A and B are in a Row, and A has scale=2, and B has scale=1, A will be twice as wide as B. Should be an integer. scale applies in Rows, and to top-level Components in Blocks where fill_height=True.'}, 'min_width': {'type': 'int', 'default': '160', 'description': 'minimum pixel width, will wrap if not sufficient screen space to satisfy this value. If a certain scale value results in this Component being narrower than min_width, the min_width parameter will be respected first.'}, 'interactive': {'type': 'bool | None', 'default': 'None', 'description': 'if True, will be rendered as an editable textbox; if False, editing will be disabled. If not provided, this is inferred based on whether the component is used as an input or output.'}, 'visible': {'type': 'bool', 'default': 'True', 'description': 'If False, component will be hidden.'}, 'elem_id': {'type': 'str | None', 'default': 'None', 'description': 'An optional string that is assigned as the id of this component in the HTML DOM. Can be used for targeting CSS styles.'}, 'autofocus': {'type': 'bool', 'default': 'False', 'description': 'If True, will focus on the textbox when the page loads. Use this carefully, as it can cause usability issues for sighted and non-sighted users.'}, 'autoscroll': {'type': 'bool', 'default': 'True', 'description': 'If True, will automatically scroll to the bottom of the textbox when the value changes, unless the user scrolls up. If False, will not scroll to the bottom of the textbox when the value changes.'}, 'elem_classes': {'type': 'list[str] | str | None', 'default': 'None', 'description': 'An optional list of strings that are assigned as the classes of this component in the HTML DOM. Can be used for targeting CSS styles.'}, 'render': {'type': 'bool', 'default': 'True', 'description': 'If False, component will not render be rendered in the Blocks context. Should be used if the intention is to assign event listeners now but render the component later.'}, 'key': {'type': 'int | str | None', 'default': 'None', 'description': 'if assigned, will be used to assume identity across a re-render. Components that have the same key across a re-render will have their value preserved.'}, 'type': {'type': '"text" | "password" | "email"', 'default': '"text"', 'description': "The type of textbox. One of: 'text', 'password', 'email', Default is 'text'."}, 'text_align': {'type': '"left" | "right" | None', 'default': 'None', 'description': 'How to align the text in the textbox, can be: "left", "right", or None (default). If None, the alignment is left if `rtl` is False, or right if `rtl` is True. Can only be changed if `type` is "text".'}, 'rtl': {'type': 'bool', 'default': 'False', 'description': 'If True and `type` is "text", sets the direction of the text to right-to-left (cursor appears on the left of the text). Default is False, which renders cursor on the right.'}, 'prompts': {'type': 'list[str]', 'default': '""', 'description': None}, 'suffixes': {'type': 'list[str]', 'default': '""', 'description': None}}, 'postprocess': {'value': {'type': 'str | None', 'description': 'Expects a {str} returned from function and sets textarea value to it.'}}, 'preprocess': {'return': {'type': 'str | None', 'description': 'Passes text value as a {str} into the function.'}, 'value': None}}, 'events': {'change': {'type': None, 'default': None, 'description': 'Triggered when the value of the ClickableTextbox changes either because of user input (e.g. a user types in a textbox) OR because of a function update (e.g. an image receives a value from the output of an event trigger). See `.input()` for a listener that is only triggered by user input.'}, 'input': {'type': None, 'default': None, 'description': 'This listener is triggered when the user changes the value of the ClickableTextbox.'}, 'select': {'type': None, 'default': None, 'description': 'Event listener for when the user selects or deselects the ClickableTextbox. Uses event data gradio.SelectData to carry `value` referring to the label of the ClickableTextbox, and `selected` to refer to state of the ClickableTextbox. See EventData documentation on how to use this event data'}, 'submit': {'type': None, 'default': None, 'description': 'This listener is triggered when the user presses the Enter key while the ClickableTextbox is focused.'}, 'focus': {'type': None, 'default': None, 'description': 'This listener is triggered when the ClickableTextbox is focused.'}, 'blur': {'type': None, 'default': None, 'description': 'This listener is triggered when the ClickableTextbox is unfocused/blurred.'}}}, '__meta__': {'additional_interfaces': {}, 'user_fn_refs': {'ClickableTextbox': []}}}

abs_path = os.path.join(os.path.dirname(__file__), "css.css")

with gr.Blocks(
    css=abs_path,
    theme=gr.themes.Default(
        font_mono=[
            gr.themes.GoogleFont("Inconsolata"),
            "monospace",
        ],
    ),
) as demo:
    gr.Markdown(
"""
# `gradio_clickabletextbox`

<div style="display: flex; gap: 7px;">
<a href="https://pypi.org/project/gradio_clickabletextbox/" target="_blank"><img alt="PyPI - Version" src="https://img.shields.io/pypi/v/gradio_clickabletextbox"></a>  
</div>

Python library for easily interacting with trained machine learning models
""", elem_classes=["md-custom"], header_links=True)
    app.render()
    gr.Markdown(
"""
## Installation

```bash
pip install gradio_clickabletextbox
```

## Usage

```python

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

```
""", elem_classes=["md-custom"], header_links=True)


    gr.Markdown("""
## `ClickableTextbox`

### Initialization
""", elem_classes=["md-custom"], header_links=True)

    gr.ParamViewer(value=_docs["ClickableTextbox"]["members"]["__init__"], linkify=[])


    gr.Markdown("### Events")
    gr.ParamViewer(value=_docs["ClickableTextbox"]["events"], linkify=['Event'])




    gr.Markdown("""

### User function

The impact on the users predict function varies depending on whether the component is used as an input or output for an event (or both).

- When used as an Input, the component only impacts the input signature of the user function.
- When used as an output, the component only impacts the return signature of the user function.

The code snippet below is accurate in cases where the component is used as both an input and an output.

- **As input:** Is passed, passes text value as a {str} into the function.
- **As output:** Should return, expects a {str} returned from function and sets textarea value to it.

 ```python
def predict(
    value: str | None
) -> str | None:
    return value
```
""", elem_classes=["md-custom", "ClickableTextbox-user-fn"], header_links=True)




    demo.load(None, js=r"""function() {
    const refs = {};
    const user_fn_refs = {
          ClickableTextbox: [], };
    requestAnimationFrame(() => {

        Object.entries(user_fn_refs).forEach(([key, refs]) => {
            if (refs.length > 0) {
                const el = document.querySelector(`.${key}-user-fn`);
                if (!el) return;
                refs.forEach(ref => {
                    el.innerHTML = el.innerHTML.replace(
                        new RegExp("\\b"+ref+"\\b", "g"),
                        `<a href="#h-${ref.toLowerCase()}">${ref}</a>`
                    );
                })
            }
        })

        Object.entries(refs).forEach(([key, refs]) => {
            if (refs.length > 0) {
                const el = document.querySelector(`.${key}`);
                if (!el) return;
                refs.forEach(ref => {
                    el.innerHTML = el.innerHTML.replace(
                        new RegExp("\\b"+ref+"\\b", "g"),
                        `<a href="#h-${ref.toLowerCase()}">${ref}</a>`
                    );
                })
            }
        })
    })
}

""")

demo.launch()

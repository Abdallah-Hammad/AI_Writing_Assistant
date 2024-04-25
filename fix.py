import os
from prompt_toolkit import prompt
from pynput.keyboard import Key, Controller
import time
import pyperclip
from string import Template
from groq import Groq


controller = Controller()
api_key = os.environ.get("GROQ_API_KEY")

PROMPT_TEMPLATE = Template(
    """Fix all typos and casing and punctuation in this text, but preserve all new line characters, and return only corrected text without any preamble:
    
    $text
    
    
    """
)


def fix_text(text, model):
    prompt = PROMPT_TEMPLATE.substitute(text=text)
    client = Groq(api_key=api_key)
    completion = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=1,
        max_tokens=1024,
        top_p=1,
        stream=False,
        stop=None,
    )
    return(completion.choices[0].message.content)



def fix_current_line(model):

    controller.tap(Key.home)
    with controller.pressed(Key.shift):
        controller.tap(Key.end)

    time.sleep(0.1)
    fix_selection(model)


def fix_selection(model):

    # 1. Copy to clipboard
    with controller.pressed(Key.ctrl):
        controller.press("c")
        controller.release("c")

    # 2. Get text from clipboard
    time.sleep(0.1)
    text = pyperclip.paste()

    # 3. fix text
    fixed_text = fix_text(text, model)
    time.sleep(0.1)

    # 4. copy back to clipboard
    pyperclip.copy(fixed_text)
    time.sleep(0.1)

    # 5. Paste the text back
    with controller.pressed(Key.ctrl):
        controller.press("v")
        controller.release("v")

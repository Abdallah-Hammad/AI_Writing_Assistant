import sys
from pynput import keyboard
from fix import fix_current_line, fix_selection

model = "llama3-8b-8192"

def on_f9():
    fix_current_line(model)


def on_f10():
    fix_selection(model)
    
def exit():
  sys.exit()
  

with keyboard.GlobalHotKeys({"<120>": on_f9, "<121>": on_f10, "<27>": exit}) as h:  # F9  # F10 # ESC
    h.join()

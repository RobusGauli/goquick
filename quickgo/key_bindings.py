from prompt_toolkit.key_binding.manager import KeyBindingManager
from prompt_toolkit.keys import Keys
from prompt_toolkit.filters import Condition

_main = '''func main() {
    
}
'''

def key_bindings_registry():
    manager = KeyBindingManager()
    registry = manager.registry

    @registry.add_binding(Keys.ControlQ)
    def _(event):
        event.cli.set_return_value(None)
    
    @registry.add_binding(Keys.Tab)
    def __(event):
        buff = event.cli.current_buffer
        buff.insert_text(' ' * 4)
    
    @registry.add_binding(Keys.F4)
    def ___(event):
        
        buff = event.cli.current_buffer
        text = buff.document.text
        new_text = ''
        if text:
            new_text = '\n'.join('import "%s"' % t for t in text.split()) + '\n'
            
        buff.delete_before_cursor(len(text))
        buff.insert_text(new_text + _main,  move_cursor=False)
        buff.cursor_down(1 + len(text.split()))
        buff.cursor_right(4)

    return registry
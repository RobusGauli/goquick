import re
from prompt_toolkit.key_binding.manager import KeyBindingManager
from prompt_toolkit.keys import Keys
from prompt_toolkit.filters import Condition

import_shortcut_regex = re.compile(r'([a-z]+)\.')
imports = lambda text: import_shortcut_regex.findall(text)

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
        doc = buff.document
        if doc.cursor_position_row == 0:
            _all_imports = imports(doc.text)
            if _all_imports:
                buff.delete_before_cursor(len(doc.text))
                buff.insert_text('\n'.join('import "%s"' %i for i in _all_imports))
                return
        
        if doc.current_line.strip() == 'main':
            buff.delete_before_cursor(len(doc.current_line))
            buff.insert_text(_main, move_cursor=False)
            buff.cursor_down(count=1)
            buff.cursor_right(count=4)
            
            return
        
        buff.insert_text(' ' * 4)
        
    
    @registry.add_binding(Keys.F4)
    def ___(event):
        
        buff = event.cli.current_buffer
        text = buff.document.text
        new_text = ''
        if text:
            new_text = '\n'.join('import "%s"' % t for t in text.split()) + '\n'
            
        buff.delete_before_cursor(len(text))
        buff.insert_text(new_text,  move_cursor=True)
        #buff.cursor_down(1 + len(text.split()))
        #buff.cursor_right(4)

    return registry
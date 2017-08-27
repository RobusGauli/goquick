from prompt_toolkit.key_binding.manager import KeyBindingManager
from prompt_toolkit.keys import Keys
from prompt_toolkit.filters import Condition

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
        buff.always_multiline = not buff.always_multiline

    return registry
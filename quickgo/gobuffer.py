from prompt_toolkit.buffer import Buffer
from prompt_toolkit.filters import Condition


class GoBuffer(Buffer):

    def __init__(self, always_multiline, *args, **kwargs):
        self.always_multiline = always_multiline
        self.return_count = 0

        @Condition
        def is_multiline():
            text = self.document.text
            return (
                self.always_multiline or
                not GoBuffer.multiline_evaluator(text)
            )
        
        super(self.__class__, self).__init__(*args, is_multiline=is_multiline, **kwargs)
    
    @staticmethod
    def multiline_evaluator(text):
        text = text.strip()
        return (
            text.endswith(';;') or 
            (text == 'exit') or
            (text == 'quit') or
            (text == ':q') 
        ) 

        
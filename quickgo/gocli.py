import itertools
from prompt_toolkit.interface import CommandLineInterface
from prompt_toolkit.application import Application
from prompt_toolkit.shortcuts import create_eventloop, create_prompt_layout, print_tokens
from prompt_toolkit.layout.lexers import PygmentsLexer
from prompt_toolkit.buffer import AcceptAction

from pygments.lexers.go import GoLexer
from pygments.token import Token

from quickgo.gobuffer import GoBuffer
from quickgo.gostyle import get_style
from quickgo.key_bindings import key_bindings_registry
from quickgo.gotoolbar import get_toolbar_tokens

class GoCLI(object):

    def __init__(self):
        self.event_loop = create_eventloop()
        self.cli = None
    
    def __enter__(self):
        self.cli = self._build_cli()
        if self.cli:
            return self.cli
        else:
            raise ValueError('Need to build CLI instance')

    def __exit__(self, *args, **kwargs):
        #print(args, kwargs)
        self.cli = None

    def _build_cli(self):
        

        get_prompt_tokens = lambda cli: \
                            [(Token.Prompt, '\nIn [%d]: ' % cli.current_buffer.return_count)]
        get_continuation_tokens = lambda cli, width: \
                            [(Token.Continuation, '.' * (width - 1) + ' ')]

        buffer = GoBuffer(
            always_multiline=True,
            accept_action=AcceptAction.RETURN_DOCUMENT
        )
        layout = create_prompt_layout(
            lexer=PygmentsLexer(GoLexer),
            get_prompt_tokens=get_prompt_tokens,
            get_continuation_tokens=get_continuation_tokens,
            get_bottom_toolbar_tokens=get_toolbar_tokens,
            multiline=True
        )
        application = Application(
            layout=layout,
            buffer=buffer,
            style=get_style(),
            key_bindings_registry=key_bindings_registry(),
            ignore_case=True
        )
        render_title = lambda text: zip(itertools.repeat(Token), ['\nQuickGo\n', 'Author: Robus Gauli | robusgauli@gmail.com\n',text,'\n\n'])
        print_tokens(render_title('Version: Experimental 0.0.0'))
        cli = CommandLineInterface(application=application, eventloop=self.event_loop)
        return cli



        
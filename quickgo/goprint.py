import itertools
from prompt_toolkit.shortcuts import print_tokens
from prompt_toolkit.styles import style_from_dict
from pygments.token import Token

style = style_from_dict({
    Token.OutPrompt: '#9988ff',
    Token.String: '#ffffff'
})



gprint = lambda buff: lambda  text: \
        print_tokens(zip(itertools.cycle([Token.OutPrompt, Token.String]), ['Out[%d]: ' % buff.return_count, text, '\n\n']), style=style)

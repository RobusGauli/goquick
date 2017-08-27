import pygments
from pygments.token import Token
from prompt_toolkit.styles import PygmentsStyle

_STYLE = {
    Token: '#ffffff bold',
    Token.Toolbar: '#ffffff bg:#111111',
    Token.Toolbar.On: '#666666',
    Token.Toolbar.Off: '#999999',
    Token.Prompt: '#00ff00',
    Token.Continuation: '#00ff00',
    Token.String: '#00ff00 bold'
}

get_style = lambda style_name='native': PygmentsStyle.from_defaults(
    style_dict=_STYLE,
    pygments_style_cls=pygments.styles.get_style_by_name(style_name)
)
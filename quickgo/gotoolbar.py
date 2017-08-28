from pygments.token import Token

def get_toolbar_tokens(cli):

    result = []
    buff = cli.current_buffer
    multiline_text = 'Multiline: ON' if buff.always_multiline else 'Multiline: OFF' 
    if buff.always_multiline:
        result.append((Token.Toolbar.On, '[F4] %s' % multiline_text))
        result.append((Token.Toolbar.On, '   [*] ";;" to Return'))
    else:
        result.append((Token.Toolbar.Off, '[F4] %s' % multiline_text))
    return result

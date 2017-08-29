from pygments.token import Token

def get_toolbar_tokens(cli):

    result = []
    buff = cli.current_buffer
    multiline_text = 'Quick Go' 
    if buff.always_multiline:
        result.append((Token.Toolbar.On, ' [*] ";;" to Return'))
        result.append((Token.Toolbar.Off, '    [F4] %s' % multiline_text))
    else:
        result.append((Token.Toolbar.Off, '[F4] %s' % multiline_text))
    return result

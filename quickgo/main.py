import collections
import click
import subprocess
import sys
import re
from quickgo.gocli import GoCLI
from quickgo.goprint import gprint
from prompt_toolkit.shortcuts import clear

err_regex = re.compile(r'(?:(?::\d)+)?:([:a-z"\. \'A-Z,]+)')
format_error = lambda text: '\n'.join(s for s in err_regex.findall(text)).strip()

class rdict(dict):

    def __getattr__(self, key):
        return self[key]
    
    def __setattr__(self, key, val):
        self[key] = val

class ImportNode:

    def __init__(self):
        self.imports = set()
    
    def add_import(self, import_statement):
        self.imports.add(import_statement)
    
    def code(self):
        return '\n'.join(import_line for import_line in self.imports)

class MainStatementNode:

    def __init__(self):
        self.main_statements = []
    
    def add_main_statements(self, statement):
        self.main_statements.append(statement)
    
    def code(self):
        return '\n'.join(st_line for st_line in self.main_statements)


class ExperimentalRepl:
    '''This is an attempt to make interactive REPL. The code here might break'''
    
    def __init__(self):
        self._state = rdict()
        #initiate import tree
        self._state.import_node = ImportNode()
        self._state.main_statement_node = MainStatementNode()
        self._state.statement_node = None

        self.code_stack = collections.deque()
        self._file_name = 'test.go'

        #a current running _state
        self._current_state = rdict()
        self._current_state.import_node = ImportNode()
        self._current_state.main_statement_node = MainStatementNode()
        self._current_state.statement_node = None
    

    def generate_code(self):
        self._clear_fmt_prints()
        return (
            'package main\n'
            'import "fmt"\n'
            '%s\n'
            'func main() {'
            '%s\n'
            '%s\n'
            '}'
        ) % (
            '\n'.join(self._state.import_node.imports.union(self._current_state.import_node.imports)),
            self._state.main_statement_node.code(),
            self._current_state.main_statement_node.code()
        )
    
    def _clear_fmt_prints(self):
        self._state.main_statement_node.main_statements = \
            [stat for stat in self._state.main_statement_node.main_statements if not stat.startswith('fmt.Println')]
    
    def _write_to_file(self):
        _file = open(self._file_name, mode='w+')
        _file.write(self.generate_code())
        _file.close()

    def merge_state(self):
        self._state.import_node.imports.update(self._current_state.import_node.imports)
        self._state.main_statement_node.main_statements.extend(self._current_state.main_statement_node.main_statements)
    
    def execute(self):
        return_code = subprocess.call('go run test.go'.split(), stdout=sys.stdin, stderr=sys.stderr)
        if return_code == 0:
            self.merge_state()
        else:
            print(return_code)
        self._current_state.import_node.imports.clear()
        self._current_state.main_statement_node.main_statements.clear()
    
    def evaluate(self, text):
        # if text.startswith('import'):
        #     self._current_state.import_node.add_import(text)
        # else:
        #     self._current_state.main_statement_node.add_main_statements(text)
        
        #now write to the _file
        
        self._write_to_file()
        self.execute()
        

def repl(code, file_name=None):
    if not file_name:
        file_name = 'temp.go'
    _command = 'go run %s' % file_name
    def generate_code():
        return (
            'package main\n'
            '%s'
        ) % code

    def write_to_file():
        _file = open(file_name, mode='w')
        _file.write(generate_code())
        _file.close()

    def execute():
        return_code, output = subprocess.getstatusoutput(_command)
        return output if return_code == 0 else format_error(output.strip())

    def evaluate():
        write_to_file()
        output = execute()
        return output
    r = rdict()
    r.evaluate = evaluate
    return r    

def evaluate_exit_cond(doc):
    if not doc:
        return True, 'Goodbye!!'
    text = doc.text.strip()

    if text in ['quit', 'exit', ':q', 'quit()', 'exit()']:
        return True, 'Goodbye!!!'
    return False, None

def main():
    global gprint
    with GoCLI() as cli:
        gprint = gprint(cli.current_buffer)
        while True:
            doc = cli.run()
            err, message = evaluate_exit_cond(doc)
            if err:
                gprint(message)
                break
            if doc.text == 'clear':
                clear()
                continue
            response = repl(doc.text.strip().rstrip(';;'), file_name='test.go')
            result = response.evaluate()
            gprint(result)

            #gprint(response)
            
            #if line breaks then increase the counter
            cli.current_buffer.inc()
            #goprint(doc.text)
            
            

            

if __name__ == '__main__':
    main()

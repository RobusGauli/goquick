import click
from quickgo.gocli import GoCLI
from quickgo.goprint import goprint

def evaluate_exit_cond(doc):
    if not doc:
        return True, 'Goodbye!!'
    text = doc.text.strip()
    if text in ['quit', 'exit', ':q', 'quit()', 'exit()']:
        return True, 'Goodbye!!!'
    return False, None

def main():
    with GoCLI() as cli:
        while True:
            doc = cli.run()
            err, message = evaluate_exit_cond(doc)
            if err:
                print(message)
                break
            goprint( cli.current_buffer.return_count, doc.text)
            #if line breaks then increase the counter
            cli.current_buffer.return_count += 1
            #goprint(doc.text)
            
            

            

if __name__ == '__main__':
    main()

from quickgo.gocli import GoCLI
from prompt_toolkit.shortcuts import print_tokens

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
            #if line breaks then increase the counter
            cli.current_buffer.return_count += 1
            print(doc.text)

            

if __name__ == '__main__':
    main()

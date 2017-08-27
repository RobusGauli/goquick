from quickgo.gocli import GoCLI

def main():
    with GoCLI() as cli:
        doc = cli.run()

if __name__ == '__main__':
    main()
    
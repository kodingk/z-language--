from parser import Parser

if __name__ == "__main__":
    filename = 'input.txt'

    env = {}
    with open(filename, 'r') as file:
        parser = Parser(file.read())

        while True:
            stmt = parser.parse_statement()
            if stmt is None:
                break
            stmt.run(env)

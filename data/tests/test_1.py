class Token:
    def __init__(self, type_, value=None):
        self.type = type_
        self.value = value

    def __repr__(self):
        return f"Token({self.type}, {repr(self.value)})"

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = text[self.pos] if text else None

    def advance(self):
        self.pos += 1
        self.current_char = self.text[self.pos] if self.pos < len(self.text) \
        else None

    def skip_whitespace(self):
        while self.current_char and self.current_char.isspace():
            self.advance()

    def number(self):
        result = ''
        while self.current_char and (self.current_char.isdigit() or \
        self.current_char == '.'):
            result += self.current_char
            self.advance()
        return float(result) if '.' in result else int(result)

    def get_next_token(self):
        while self.current_char:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
            if self.current_char.isdigit():
                return Token('NUMBER', self.number())
            if self.current_char in '+-*/()':
                token = Token(self.current_char)
                self.advance()
                return token
            raise ValueError(f"Invalid character: {self.current_char}")
        return Token('EOF')

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def eat(self, token_type): # ELIMINADA
        if self.current_token.type == token_type: # ELIMINADA
            self.current_token = self.lexer.get_next_token() # ELIMINADA
        else: # ELIMINADA
            raise ValueError(f"Expected token {token_type}, got \
            {self.current_token.type}") # ELIMINADA (las 2 líneas previas cuentan como 1)

    def factor(self):
        token = self.current_token
        if token.type == 'NUMBER':
            self.eat('NUMBER')
            return token.value
        elif token.type == '(':
            self.eat('(')
            result = self.expr()
            self.eat(')')
            return result
        raise ValueError(f"Unexpected token in factor: {token}")

    def term(self):
        result = self.factor()
        while self.current_token.type in ('*', '/'):
            token = self.current_token
            if token.type == '*':
                self.eat('*')
                result *= self.factor()
            elif token.type == '/':
                self.eat('/')
                result /= self.factor()
        return result

    def expr(self):
        result = self.term()
        while self.current_token.type in ('+', '-'):
            token = self.current_token
            if token.type == '+':
                self.eat('+')
                result += self.term()
            elif token.type == '-':
                self.eat('-')
                result -= self.term()
        return result

def main():
    while True:
        try:
            text = input("calc> ")
            if text.lower() in {'exit', 'quit'}:
                break
            lexer = Lexer(text)
            parser = Parser(lexer)
            result = parser.expr()
            print(f"Result: {result}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()

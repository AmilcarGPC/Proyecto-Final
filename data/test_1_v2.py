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

    ## # AGREGADA TOTALMENTE NUEVA # AGREGADA TOTALMENTE NUEVA

    def factor(self): # AGREGADA TOTALMENTE NUEVA
        token = self.current_token # AGREGADA TOTALMENTE NUEVA
        if token.type == 'NUMBER': # AGREGADA TOTALMENTE NUEVA
            self.eat('NUMBER') # AGREGADA TOTALMENTE NUEVA
            return token.value # AGREGADA TOTALMENTE NUEVA
        elif token.type == '(': # AGREGADA TOTALMENTE NUEVA
            self.eat('(') # AGREGADA TOTALMENTE NUEVA
            result = self.expr() # AGREGADA TOTALMENTE NUEVA
            self.eat(')') # AGREGADA TOTALMENTE NUEVA
            return result # AGREGADA TOTALMENTE NUEVA
        raise ValueError(f"Unexpected token in factor: {token}") # AGREGADA TOTALMENTE NUEVA

    def term(self): # AGREGADA TOTALMENTE NUEVA
        result = self.factor() # AGREGADA TOTALMENTE NUEVA
        while self.current_token.type in ('*', '/'): # AGREGADA TOTALMENTE NUEVA
            token = self.current_token # AGREGADA TOTALMENTE NUEVA
            if token.type == '*': # AGREGADA TOTALMENTE NUEVA
                self.eat('*') # AGREGADA TOTALMENTE NUEVA
                result *= self.factor() # AGREGADA TOTALMENTE NUEVA
            elif token.type == '/': # AGREGADA TOTALMENTE NUEVA
                self.eat('/') # AGREGADA TOTALMENTE NUEVA
                result /= self.factor() # AGREGADA TOTALMENTE NUEVA
        return result # AGREGADA TOTALMENTE NUEVA

    def expr(self): # AGREGADA TOTALMENTE NUEVA
        result = self.term() # AGREGADA TOTALMENTE NUEVA
        while self.current_token.type in ('+', '-'): # AGREGADA TOTALMENTE NUEVA
            token = self.current_token # AGREGADA TOTALMENTE NUEVA
            if token.type == '+': # AGREGADA TOTALMENTE NUEVA
                self.eat('+') # AGREGADA TOTALMENTE NUEVA
                result += self.term() # AGREGADA TOTALMENTE NUEVA
            elif token.type == '-': # AGREGADA TOTALMENTE NUEVA
                self.eat('-') # AGREGADA TOTALMENTE NUEVA
                result -= self.term() # AGREGADA TOTALMENTE NUEVA
        return result # AGREGADA TOTALMENTE NUEVA
    
    def eat(self, token_type): # AGREGADA TOTALMENTE NUEVA # AGREGADA PEQUEÑA MODIFICACIÓN DEL 0.72%
        if self.current_token.type == token_type: # AGREGADA TOTALMENTE NUEVA # AGREGADA PEQUEÑA MODIFICACIÓN DEL 0.79%
            self.current_token = self.lexer.get_next_token() # AGREGADA \
            TOTALMENTE NUEVA # AGREGADA PEQUEÑA MODIFICACIÓN DEL 0.8% (las 2 líneas previas cuentan como 1)
        else: # AGREGADA TOTALMENTE NUEVA # AGREGADA TOTALMENTE NUEVA
            raise ValueError(f"Expected token {token_type}, got \
            {self.current_token.type}") # AGREGADA TOTALMENTE NUEVA (las 2 \
            líneas previas cuentan como 1)

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
    main() # AGREGADA TOTALMENTE NUEVA (las 19 líneas previas cuentan como 1)

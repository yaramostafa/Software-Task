import json
import re
from operations import AddOperation, SubOperation, MulOperation, DivOperation
from database import SQLiteDataSink

# Token types
INTEGER, PLUS, MINUS, MUL, DIV, LPAREN, RPAREN, EOF, ATTR, REGEX, COMMA, STRING = (
    'INTEGER', 'PLUS', 'MINUS', 'MUL', 'DIV', '(', ')', 'EOF', 'ATTR', 'REGEX', 'COMMA', 'STRING'
)


class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return f'Token({self.type}, {repr(self.value)})'

    def __repr__(self):
        return self.__str__()


class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]

    def error(self):
        raise Exception('Invalid character')

    def advance(self):
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def integer(self):
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    # for regex
    def string(self):
        result = ''
        self.advance()  # skip the opening quote
        while self.current_char is not None and self.current_char != '"':
            result += self.current_char
            self.advance()
        self.advance()  # skip the closing quote
        return result

    def get_next_token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit():
                return Token(INTEGER, self.integer())

            if self.current_char.isalpha():
                word = ''
                while self.current_char is not None and self.current_char.isalnum():
                    word += self.current_char
                    self.advance()
                if word == 'Regex':
                    return Token(REGEX, word)
                elif word == 'ATTR':
                    return Token(ATTR, word)

            if self.current_char == '+':
                self.advance()
                return Token(PLUS, '+')

            if self.current_char == '-':
                self.advance()
                return Token(MINUS, '-')

            if self.current_char == '*':
                self.advance()
                return Token(MUL, '*')

            if self.current_char == '/':
                self.advance()
                return Token(DIV, '/')

            if self.current_char == '(':
                self.advance()
                return Token(LPAREN, '(')

            if self.current_char == ')':
                self.advance()
                return Token(RPAREN, ')')

            if self.current_char == ',':
                self.advance()
                return Token(COMMA, ',')

            if self.current_char == '"':
                return Token(STRING, self.string())

            self.error()

        return Token(EOF, None)


class AST:
    pass


class BinOp(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right


class Num(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value


class Regex(AST):
    def __init__(self, attr, pattern):
        self.attr = attr
        self.pattern = pattern


class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()
        self.attr_value = None

    def error(self):
        raise Exception('Invalid syntax')

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def factor(self):
        token = self.current_token
        if token.type == INTEGER:
            self.eat(INTEGER)
            return Num(token)
        elif token.type == ATTR:  # handles ATTR as a variable
            self.eat(ATTR)
            return Num(Token(INTEGER, self.attr_value))  # use attr_value as its numeric value
        elif token.type == LPAREN:
            self.eat(LPAREN)
            node = self.expr()
            self.eat(RPAREN)
            return node
        elif token.type == REGEX:
            return self.regex()
        else:
            self.error()

    def regex(self):
        self.eat(REGEX)
        self.eat(LPAREN)
        attr = self.current_token
        self.eat(ATTR)
        self.eat(COMMA)
        pattern = self.current_token
        self.eat(STRING)
        self.eat(RPAREN)
        return Regex(attr, pattern)

    def term(self):
        node = self.factor()
        while self.current_token.type in (MUL, DIV):
            token = self.current_token
            if token.type == MUL:
                self.eat(MUL)
            elif token.type == DIV:
                self.eat(DIV)
            node = BinOp(left=node, op=token, right=self.factor())
        return node

    def expr(self):
        node = self.term()
        while self.current_token.type in (PLUS, MINUS):
            token = self.current_token
            if token.type == PLUS:
                self.eat(PLUS)
            elif token.type == MINUS:
                self.eat(MINUS)
            node = BinOp(left=node, op=token, right=self.term())
        return node

    def parse(self):
        return self.expr()


class NodeVisitor:
    def visit(self, node):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception(f'No visit_{type(node).__name__} method')


class Interpreter(NodeVisitor):
    def __init__(self, parser, attr_value):
        self.parser = parser
        self.attr_value = attr_value
        self.operations = {
            'PLUS': AddOperation(),
            'MINUS': SubOperation(),
            'MUL': MulOperation(),
            'DIV': DivOperation()
        }

    def visit_BinOp(self, node):
        operation = self.operations.get(node.op.type)
        if operation:
            return operation.apply(self.visit(node.left), self.visit(node.right))
        else:
            raise ValueError(f"Unsupported operation: {node.op.type}")

    def visit_Num(self, node):
        return node.value

    def visit_Regex(self, node):
        pattern = node.pattern.value
        return str(bool(re.match(pattern, self.attr_value)))

    def interpret(self):
        tree = self.parser.parse()
        return self.visit(tree)


# class FileDataSource:
#     def __init__(self, input_file):
#         self.input_file = input_file
#
#     def read_messages(self):
#         with open(self.input_file, "r") as file:
#             for record in file:
#                 record = record.strip()
#                 if record:
#                     yield record



def process_message(message, equation):
    message_obj = json.loads(message)
    attr_value = message_obj.get("value", "")  # get returns default value if not found

    # Check if attr_value is numeric
    try:
        numeric_value = float(attr_value)
    except ValueError:
        numeric_value = None

    lexer = Lexer(equation)
    parser = Parser(lexer)

    try:
        if "Regex" in equation:  # handles regex equations
            interpreter = Interpreter(parser, attr_value)
        else:  # handles arithmetic equations
            if numeric_value is None:
                raise ValueError(f"Non-numeric value '{attr_value}' cannot be used in arithmetic equations")
            parser.attr_value = numeric_value  # Pass numeric value to parser
            interpreter = Interpreter(parser, str(numeric_value))

        tree = parser.parse()
        if tree is None:  # ensuring tree is valid
            raise Exception("Failed to parse equation: Invalid AST")

        result = interpreter.visit(tree)

        output_message = {
            "asset_id": message_obj["asset_id"],
            "attribute_id": "output_" + message_obj["attribute_id"],
            "timestamp": message_obj["timestamp"],
            "value": result
        }
        return output_message

    except Exception as e:
        raise Exception(f"Error processing message: {e}")


def main():
    input_file = "data.txt"
    db_name = "processed_data.db"

    # reading equation from config.txt
    with open("config.txt", "r") as config_file:
        equation = config_file.read().strip()

    # initializing data sink for SQLite
    data_sink = SQLiteDataSink(db_name)

    try:
        with open(input_file, "r") as file:
            records = file.readlines()

        for record in records:
            record = record.strip()
            if not record:
                continue

            try:
                output_message = process_message(record, equation)
                data_sink.write_message(output_message)  # writes to SQLite database
                print(output_message)
            except Exception as e:
                print(f"Error processing record: {record}, Error: {e}")

    finally:
        data_sink.close()  # ensures database connection is closed

if __name__ == "__main__":
    main()
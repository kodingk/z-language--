from tokens import Tokenizer, Token
from statement import Statement, ExpressionStatement, BeginStatement, RepeatStatement, PrintStatement, AssignStatement

class Parser:
    def __init__(self, src: str):
        self.tokenizer = Tokenizer(src)  # 다음 토큰을 받아 오는 Tokenizer 객체

    def parse_statement(self) -> Statement | None:
        """
        임의의 구문을 파싱하는 메서드.
        self.tokenizer 이터레이터를, 해당 구문의 마지막 토큰까지 소비함.
        """
        token = self.tokenizer.peek()
        if token is None:
            return None

        match token[0]:
            case Token.BEGIN:
                return self.parse_begin()
            case Token.REPEAT:
                return self.parse_repeat()
            case Token.PRINT:
                return self.parse_print()
            case Token.VARIABLE:
                return self.parse_assign()

        raise SyntaxError(f"잘못된 토큰입니다: {token}")

    def parse_begin(self) -> BeginStatement:
        """
        BEGIN 구문을 파싱하는 메서드.
        self.tokenizer 이터레이터를, 대응되는 STOP 토큰까지 소비함.
        """
        assert next(self.tokenizer)[0] == Token.BEGIN, "BEGIN 토큰이 없습니다."

        statements = []
        while True:
            peeked = self.tokenizer.peek()
            if peeked is None:
                raise SyntaxError("STOP 토큰이 없습니다.")
            if peeked[0] == Token.STOP:
                next(self.tokenizer)  # STOP 토큰을 소비함.
                break
            statements.append(self.parse_statement())

        return BeginStatement(statements)

    def parse_repeat(self) -> RepeatStatement:
        """
        REPEAT 구문을 파싱하는 메서드.
        self.tokenizer 이터레이터를, 대응되는 STOP 토큰까지 소비함.
        """
        assert next(self.tokenizer)[0] == Token.REPEAT, "REPEAT 토큰이 없습니다."

        token = next(self.tokenizer)
        if token[0] != Token.NUMBER:
            raise SyntaxError(f"반복 횟수를 숫자로 입력해야 합니다: {token}")

        count = int(token[1][0])
        statements = []
        while True:
            peeked = self.tokenizer.peek()
            if peeked is None:
                raise SyntaxError("STOP 토큰이 없습니다.")
            if peeked[0] == Token.STOP:
                next(self.tokenizer)  # STOP 토큰을 소비함.
                break
            statements.append(self.parse_statement())

        return RepeatStatement(statements, count)

    def parse_print(self) -> PrintStatement:
        """
        PRINT 구문을 파싱하는 메서드.
        self.tokenizer 이터레이터를, 대응되는 변수 이름까지 소비함.
        """
        assert next(self.tokenizer)[0] == Token.PRINT, "PRINT 토큰이 없습니다."

        token = next(self.tokenizer)
        if token[0] != Token.VARIABLE:
            raise SyntaxError(f"잘못된 토큰입니다: {token}")

        variable = token[1][0]
        return PrintStatement(variable)

    def parse_assign(self) -> AssignStatement:
        """
        ASSIGN 구문을 파싱하는 메서드.
        self.tokenizer 이터레이터를, 대응되는 변수 이름까지 소비함.
        """
        token = next(self.tokenizer)
        if token[0] != Token.VARIABLE:
            raise SyntaxError(f"잘못된 토큰입니다: {token}")
        variable = token[1][0]

        assert next(self.tokenizer)[0] == Token.ASSIGN, "ASSIGN 토큰이 없습니다."

        expression = self.parse_expression()

        return AssignStatement(variable, expression)

    def parse_expression(self) -> ExpressionStatement:
        """
        expression을 파싱하는 메서드.
        해당 줄 끝까지 소비함.
        """
        tokens: list[tuple[Token, tuple[str, ...]]] = [next(self.tokenizer)]
        assert tokens[0][0] in [Token.VARIABLE, Token.MULTIPLIED_VARIABLE, Token.NUMBER], f"잘못된 토큰입니다: {tokens[0]}"

        while True:
            peeked = self.tokenizer.peek()
            if peeked is None:
                raise SyntaxError("잘못된 위치의 EOF입니다.")
            if peeked[0] in [Token.PLUS, Token.MINUS]:
                next(self.tokenizer)
                tokens.append(peeked)
                tokens.append(next(self.tokenizer))
                assert tokens[-1][0] in [Token.VARIABLE, Token.MULTIPLIED_VARIABLE, Token.NUMBER], f"잘못된 토큰입니다: {tokens[-1]}"

            else:
                break

        return ExpressionStatement(tokens)

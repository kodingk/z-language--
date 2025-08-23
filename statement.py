from token import Token


EVAL_BOUND = 10000


class Statement:
    def run(self, env: dict[str, int]):
        raise NotImplementedError("run 메서드가 구현되지 않았습니다.")


class BeginStatement(Statement):
    def __init__(self, statements: list[Statement]):
        self.statements = statements

    def run(self, env: dict[str, int]):
        env.clear()
        for statement in self.statements:
            statement.run(env)


class RepeatStatement(Statement):
    def __init__(self, statements: list[Statement], count: int):
        self.statements = statements
        self.count = count

    def run(self, env: dict[str, int]):
        for _ in range(self.count):
            for statement in self.statements:
                statement.run(env)


class ExpressionStatement(Statement):
    def __init__(self, tokens: list[tuple[Token, tuple[str, ...]]]):
        self.tokens = tokens

    def run(self, env: dict[str, int]) -> int:
        idx = 0
        value = self.eval_unit(env, idx)
        while idx + 1 < len(self.tokens):
            if self.tokens[idx + 1][0] == Token.PLUS:
                value += self.eval_unit(env, idx + 2)
                idx += 2
            elif self.tokens[idx + 1][0] == Token.MINUS:
                value -= self.eval_unit(env, idx + 2)
                idx += 2
            else:
                raise ValueError(f'유효하지 않은 토큰입니다: {self.tokens[idx + 1]}')

        return value

    def eval_unit(self, env: dict[str, int], token_idx: int) -> int:
        token = self.tokens[token_idx]
        if token[0] == Token.NUMBER:
            return int(token[1][0]) % EVAL_BOUND
        elif token[0] == Token.VARIABLE:
            return env[token[1][0]] % EVAL_BOUND
        elif token[0] == Token.MULTIPLIED_VARIABLE:
            coeff = int(token[1][0])
            var_name = token[1][1]
            return coeff * env[var_name] % EVAL_BOUND

        raise ValueError(f'유효하지 않은 토큰입니다: {token}')


class AssignStatement(Statement):
    def __init__(self, var_name: str, expression: ExpressionStatement):
        self.var_name = var_name
        self.expression = expression

    def run(self, env: dict[str, int]):
        value = self.expression.run(env)
        env[self.var_name] = value


class PrintStatement(Statement):
    def __init__(self, var_name: str):
        self.var_name = var_name

    def run(self, env: dict[str, int]):
        print(f'{self.var_name} = {env[self.var_name]}')

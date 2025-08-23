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
        """
        힌트:
          - 내부 문장들을 count 번 실행한다.
          - BeginStatement 의 동작 과정을 이해하도록 한다. 
        """
        raise NotImplementedError("RepeatStatement.run을 구현한다.")


class ExpressionStatement(Statement):
    def __init__(self, tokens: list[tuple[Token, tuple[str, ...]]]):
        self.tokens = tokens

    def run(self, env: dict[str, int]) -> int:
        """
        힌트:
          - parse_assign 에서 호출할 것이다. 해당 매소드에서 tokens 에 무엇이 들어가는지를 살펴본다. 
          - 토큰을 좌→우로 보며 + / - 를 적용해 값을 계산한다.
          - 개별 항은 eval_unit(...)으로 해석한다.
          - 모듈러를 사용한다. 
        """
        raise NotImplementedError("ExpressionStatement.run을 구현한다.")

    def eval_unit(self, env: dict[str, int], token_idx: int) -> int:
        """
        힌트:
          - NUMBER: 문자열 숫자를 정수로 바꾼 값.
          - VARIABLE: env에서 변수 값을 읽는다. 초기화되지 않았다면 과제 조건에 맞게 처리한다.
          - MULTIPLIED_VARIABLE: (계수, 변수명) 튜플을 이용해 계수 * 변수값.
          - 모듈러를 적용한다.
        """
        raise NotImplementedError("ExpressionStatement.eval_unit을 구현한다.")


class AssignStatement(Statement):
    def __init__(self, var_name: str, expression: ExpressionStatement):
        self.var_name = var_name
        self.expression = expression

    def run(self, env: dict[str, int]):
        """
        힌트:
          - expression.run(env)로 값을 계산해 변수에 저장한다.
          - 저장 시 0..9999 범위를 만족하도록 정규화한다(음수 포함 주의).
        """
        raise NotImplementedError("AssignStatement.run을 구현한다.")


class PrintStatement(Statement):
    def __init__(self, var_name: str):
        self.var_name = var_name

    def run(self, env: dict[str, int]):
        """
        힌트:
          - 출력 형식은 'a = 1234' 와 같다. 
        """
        raise NotImplementedError("PrintStatement.run을 구현한다.")
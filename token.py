import enum
import re

VAR_REGEX = re.compile(r'[a-z]')
NUM_REGEX = re.compile(r'\d+')
MULTIPLIED_VAR_REGEX = re.compile(r'(\d+)([a-z])')

class Token(enum.Enum):
    # 키워드
    BEGIN = 0
    REPEAT = 1
    STOP = 2
    PRINT = 3

    # 연산자
    PLUS = 4
    MINUS = 5
    ASSIGN = 6

    # 변수 및 리터럴
    VARIABLE = 7
    NUMBER = 8
    MULTIPLIED_VARIABLE = 9  # e.g. 2x, 3a

class Tokenizer:
    """
    주어진 문자열을 token 단위로 나누어 반환하는 클래스.
    """

    def __init__(self, src: str):
        self.src = src

    def __iter__(self):
        return self

    def __next__(self) -> tuple[Token, tuple[str, ...]] :
        """
        다음 등장하는 토큰을 반환. (토큰, 실제 문자열 구간)의 형식으로 반환함.
        다음 토큰이 없을 경우 StopIteration 예외를 발생.
        """

        self.src = self.src.strip()  # 공백으로 시작하지 않음을 보장.
        if len(self.src) == 0:
            raise StopIteration

        # ------------------------------------------------------------
        # 키워드
        # ------------------------------------------------------------

        if self.src.startswith('BEGIN'):
            self.src = self.src[len('BEGIN'):].strip()
            return Token.BEGIN, ('BEGIN',)

        if self.src.startswith('REPEAT'):
            self.src = self.src[len('REPEAT'):].strip()
            return Token.REPEAT, ('REPEAT',)

        if self.src.startswith('STOP'):
            self.src = self.src[len('STOP'):].strip()
            return Token.STOP, ('STOP',)

        if self.src.startswith('PRINT'):
            self.src = self.src[len('PRINT'):].strip()
            return Token.PRINT, ('PRINT',)

        # ------------------------------------------------------------
        # 연산자
        # ------------------------------------------------------------

        if self.src.startswith('+'):
            self.src = self.src[len('+'):].strip()
            return Token.PLUS, ('+',)

        if self.src.startswith('-'):
            self.src = self.src[len('-'):].strip()
            return Token.MINUS, ('-',)

        if self.src.startswith('='):
            self.src = self.src[len('='):].strip()
            return Token.ASSIGN, ('=',)

        # ------------------------------------------------------------
        # 변수 및 숫자 - 주의: 숫자를 판별하기 전에 곱해진 변수인지 확인해야 함.
        # ------------------------------------------------------------

        var = VAR_REGEX.match(self.src)
        if var is not None:
            var_name = var.group()
            print(f"var_name {var_name}")
            self.src = self.src[len(var_name):].strip()
            return Token.VARIABLE, (var_name,)

        multiplied_var = MULTIPLIED_VAR_REGEX.match(self.src)
        if multiplied_var is not None:
            # groups는 (계수, 변수)의 튜플 형식으로 이루어짐.
            group, groups = multiplied_var.group(), multiplied_var.groups()
            self.src = self.src[len(group):].strip()
            return Token.MULTIPLIED_VARIABLE, groups

        num = NUM_REGEX.match(self.src)
        if num is not None:
            num_value = num.group()
            self.src = self.src[len(num_value):].strip()
            return Token.NUMBER, (num_value,)

        # 빈 문자열이면 [] 이어서 오류가 날 수 있지만, 이건 맨 윗 코드에서 strip을 해주기 때문에 오류가 날 일은 없음.
        raise ValueError(f'정의되지 않은 토큰입니다: {self.src.split()[0]}')

    def peek(self) -> tuple[Token, tuple[str, ...]] | None:
        """
        다음 등장하는 토큰을 반환. (토큰, 실제 문자열 구간)의 형식으로 반환함.
        __next__와는 달리, self.src를 수정하지 않음. (공백 제외)
        다음 토큰이 없을 경우 None을 반환.
        """

        self.src = self.src.strip()  # 공백으로 시작하지 않음을 보장.
        if len(self.src) == 0:
            return None

        # ------------------------------------------------------------
        # 키워드
        # ------------------------------------------------------------

        if self.src.startswith('BEGIN'):
            return Token.BEGIN, ('BEGIN',)

        if self.src.startswith('REPEAT'):
            return Token.REPEAT, ('REPEAT',)

        if self.src.startswith('STOP'):
            return Token.STOP, ('STOP',)

        if self.src.startswith('PRINT'):
            return Token.PRINT, ('PRINT',)

        # ------------------------------------------------------------
        # 연산자
        # ------------------------------------------------------------

        if self.src.startswith('+'):
            return Token.PLUS, ('+',)

        if self.src.startswith('-'):
            return Token.MINUS, ('-',)

        if self.src.startswith('='):
            return Token.ASSIGN, ('=',)

        # ------------------------------------------------------------
        # 변수 및 숫자 - 주의: 숫자를 판별하기 전에 곱해진 변수인지 확인해야 함.
        # ------------------------------------------------------------

        var = VAR_REGEX.match(self.src)
        if var is not None:
            var_name = var.group()
            return Token.VARIABLE, (var_name,)

        multiplied_var = MULTIPLIED_VAR_REGEX.match(self.src)
        if multiplied_var is not None:
            # groups는 (계수, 변수)의 튜플 형식으로 이루어짐.
            return Token.MULTIPLIED_VARIABLE, multiplied_var.groups()

        num = NUM_REGEX.match(self.src)
        if num is not None:
            num_value = num.group()
            return Token.NUMBER, (num_value,)

        # 빈 문자열이면 [] 이어서 오류가 날 수 있지만, 이건 맨 윗 코드에서 strip을 해주기 때문에 오류가 날 일은 없음.
        raise ValueError(f'정의되지 않은 토큰입니다: {self.src.split()[0]}')

# Programming Language Z Interpreter

이 프로젝트는 [BOJ 3203번 문제](https://www.acmicpc.net/problem/3203)를 기반으로 한다.  
추가 조건으로 전체 `REPEAT` 횟수의 곱은 **1,000,000 이하**라 가정하고, **초기화되지 않은 변수를 사용하면 에러를 발생**시키도록 한다.

---

## 실행 흐름

### 1. `token.py`
- 문자열을 **토큰 단위로 분리**하는 **Tokenizer**를 정의한다.
- **Token enum**: 프로그램에서 사용할 토큰 종류
  - 키워드: `BEGIN`, `REPEAT`, `STOP`, `PRINT`
  - 연산자: `PLUS (+)`, `MINUS (-)`, `ASSIGN (=)`
  - 피연산자: `VARIABLE`, `NUMBER`, `MULTIPLIED_VARIABLE`
- **정규식**
  - `VAR_REGEX = [a-z]`
  - `NUM_REGEX = \d+`
  - `MULTIPLIED_VAR_REGEX = (\d+)([a-z])`
- **Tokenizer 동작**
  - `__next__()`: 다음 토큰을 소비하고 반환한다.
  - `peek()`: 다음 토큰을 미리 확인하되 문자열은 그대로 둔다.  
  → 즉, 입력 소스를 하나씩 읽어 **토큰**으로 변환한다.

---

### 2. `statement.py`
- 각 문장은 `run()` 메서드를 통해 실행 동작을 정의한다.
- **구현된 클래스**
  - `BeginStatement`: BEGIN ~ STOP 블록을 실행한다.
  - `RepeatStatement`: REPEAT ~ STOP 블록을 주어진 횟수만큼 실행한다.
  - `AssignStatement`: 변수를 대입한다.
  - `PrintStatement`: 변수 값을 출력한다.
  - `ExpressionStatement`: 식을 계산한다.

---

### 3. `parser.py`
- 토큰을 받아 `Statement` 형태로 변환한다.
- 주요 메서드
  - `parse_statement()`: 다음 토큰을 보고 어떤 문장인지 판단한다.
  - `parse_begin()`: BEGIN ~ STOP 블록을 파싱한다.
  - `parse_repeat()`: REPEAT ~ STOP 블록을 파싱한다.
  - `parse_assign()`: 대입문을 파싱한다.
  - `parse_print()`: 출력문을 파싱한다.
  - `parse_expression()`: 수식을 파싱한다.
- (주의) 이때 `BEGIN`과 `REPEAT`은 내부에 여러 문장을 가질 수 있으므로 `self.parse_statement()`를 재귀적으로 호출한다.

---

### 4. `main.py`
- 프로그램의 시작점이다.
- `input.txt` 파일을 읽어 전체 소스 코드를 가져온다.
- `Parser` 객체를 생성하여 문장을 하나씩 파싱한다.
- 파싱된 문장을 실행(`stmt.run(env)`)하면서 `env`에 변수 값을 저장한다.

---

## 추가 과제

1. **Tokenizer 최적화**  
   현재 `token.py`는 `self.src = self.src.strip()` 방식으로 문자열을 잘라내기 때문에 시간복잡도가 O(n^2)이 된다 (n은 문자열 길이).  
   이를 `pos` 변수를 도입해 현재 위치만 갱신하는 방식으로 최적화한다.

2. **변수 확장**  
   현재 변수는 `[a-z]` 한 글자만 가능하다.  
   이를 `[a-zA-Z]+` 로 확장하고, 맨 앞에 숫자가 올 수 없게 하며, 필요하다면 숫자(`0-9`) 및 밑줄을 포함하도록 더 확장한다.

3. **초기화되지 않은 변수 처리**  
   현재는 초기화되지 않은 변수를 사용하면 에러를 발생시킨다.  
   이를 확장해 초기화되지 않은 변수를 사용할 때 **자동으로 0으로 초기화**되도록 한다.

4. 원본 문제 해결
- `REPEAT`이 중첩되면 단순 시뮬레이션은 불가능하다.  
- 각 `assign`은 \( x' = A x + b \pmod{10000} \) 형태의 **일차 변환**으로 볼 수 있다. (A는 행렬이고 x는 Z_10000^26 벡터이다.)
- 여러 줄은 변환 합성으로 하나의 \((A, b)\)로 표현된다.  
- `REPEAT n`은 \((A, b)^n\) 꼴의 **거듭제곱 변환**이 된다.  
- 행렬 거듭제곱은 **분할정복 (binary exponentiation)** 으로 \(O(\log n)\)에 계산한다.

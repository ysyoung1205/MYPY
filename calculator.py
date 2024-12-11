import tkinter as tk
#import datetime
import re  #파이썬 정규표현식
from decimal import Decimal #정확한 십진수연산을 도와줌

# flag
new_calculation = False
operator_clicked = False
# 키보드 입력 처리
def keypress(event):
    global new_calculation
    key = event.char

    valid_chars = "0123456789+-*/." # 유효 문자 정의

    # Backspace(백스페이스), Enter 처리용
    # event.keysym을 사용해 키심(Ksym)으로 확인
    if event.keysym == "BackSpace":  # # event.char -> event.keysym()
        backSpace()
        return "break"
    elif event.keysym == "Return":  # Enter
        calculate()
        return "break"

    # char가 없거나(예: Shift, Alt 등) 유효한 문자가 아니면 무시
    if not key or key not in valid_chars:
        return "break"

    # 유효한 문자(숫자, '.', 연산자)인 경우
    if key in "+-*/":
        # 연산자 처리
        if new_calculation:
            # 이전 결과가 남아 있다면 지우고 시작
            new_calculation = False
        operator_click(key)
    else:
        # 숫자나 '.' 입력
        if new_calculation:
            # 새 계산 시작, 이전 결과 삭제
            entry.delete(0, tk.END)
            new_calculation = False
        entry.insert(tk.END, key)

    return "break"


def button_click(number):
    global new_calculation   
    global operator_clicked
    current = entry.get()

    if new_calculation:
        entry.delete(0, tk.END)
        entry2.delete("1.0", "end")
        entry.insert(0, str(number))
        new_calculation = False
        return "break"
    
        # current2의 마지막 값이 연산자인지 확인
    if operator_clicked:  # 마지막 문자가 연산자인 경우
        entry.delete(0, tk.END)  # Entry 리셋
        current=""
        operator_clicked = False
        
    entry.delete(0, tk.END)
    entry.insert(0, current + str(number))
    print(f"Current Value: {current}")  # Text 위젯 값
    print(f"Button clicked: {number}")

    
def operator_click(operator):
    global new_calculation
    global operator_clicked
    current = entry.get()
    current2 = entry2.get("1.0", "end")
    
    if new_calculation:
        entry2.delete("1.0","end")
        #entry2.insert("1.0", current)
        new_calculation = False
    
    
    #entry.delete(0,tk.END)
    #entry.insert(0, current + operator)
    #entry2.delete("1.0", "end")
    #방금 입력한 값이 연산자인 경우  entry2에 이전에 입력한 값과 연산자 입력되게 하기
    entry2.insert("end", current + operator)
    #entry2.insert("end", operator)
    operator_clicked = True

# def percent(number):
#      current = entry.get()
#      current2 = entry2.get("1.0","end").strip() 
#      entry.delete(0,tk.END)
#      entry2.delete("end")
#      entry.insert(0, float(current)*0.01)  #연산자 뒤에 숫자만 적용되어야 함
#      entry.insert(0, float(current2)*0.01)  #연산자 뒤에 숫자만 적용되어야 함


def percent():
    current = entry.get()
    current2 = entry2.get("1.0","end")
    try:
        value = float(current) / 100 * float(current2)
        entry.delete(0, tk.END)
        entry.insert(0, str(value))
        print(f"Percent clicked: {current}% = {value}")
    except ValueError:
        entry.delete(0, tk.END)
        entry.insert(0, "Error")
        print("Invalid input for percent")
   

def clear():
    global new_calculation
    entry.delete(0, tk.END)
    entry2.delete("1.0","end")
    new_calculation = False

def backSpace():
     # 현재 텍스트 가져오기
    current_text = entry.get()
    current2 = entry2.get("1.0","end").strip()
    if current_text:  # 텍스트가 있을 경우
        last_char = current2[-1]
        print(f"Last character: {last_char}")
        # 마지막 글자를 제외한 텍스트로 업데이트
        entry.delete(0, tk.END)
        entry.insert(0, current_text[:-1])

def calculate(event=None):
    global new_calculation
    current = entry.get()
    current2 = entry2.get("1.0","end").strip()

    expr = current2 + current  #공백처리
    pattern = r"(\d+(\.\d+)?)"  # 숫자 패턴: 하나 이상의 숫자 + (선택적으로 '.' 뒤에 숫자들)
    # 정규표현식을 사용해 모든 숫자를 Decimal('...')로 감싸기
    expr_decimal = re.sub(pattern, r"Decimal('\1')", expr)
    try:
        #result = eval(entry.get())
        result = eval(expr_decimal, {"Decimal": Decimal}, {})
        entry.delete(0, tk.END)

        entry.insert(0, str(result))
        entry2.insert("end", current + "=")
        new_calculation = True
        print(new_calculation)

    except Exception:
        entry.delete(0, tk.END)
        entry.insert(0, "Error")
        new_calculation = True

# # 입력 검증 함수
# def validate_input(new_value):
#     valid_chars = "0123456789+-*/."
#     return all(char in valid_chars for char in new_value)
    
 
 # GUI 초기화
root = tk.Tk()
root.title("Calculator")

 
# 입력창에 제한 설정
#validate_cmd = root.register(validate_input)  # 검증 함수 등록
entry = tk.Entry(root, width=35, borderwidth=5, font=("default",13))
entry.grid(row=1, column=0, columnspan=4, padx=10, pady=10)

entry2 = tk.Text(root, width=35,height=5, borderwidth=5)
entry2.grid(row=0, column=0, columnspan=4, padx=10, pady=10)


# Enter 키 바인딩
#root.bind('<KeyPress>', keypress)
#root.bind('<Return>', calculate)  # 'Return'은 Enter 키
entry.bind('<Key>',keypress)
entry2.bind('<Key>',keypress)

 # 버튼 정의
button_values = [
    ('%', 2, 0), ('C', 2, 1), ('', 2, 2), ('←', 2, 3),
    ('1/χ', 3, 0), ('χ²', 3, 1), ('²√χ', 3, 2), ('/', 3, 3),
    ('7', 4, 0), ('8', 4, 1), ('9', 4, 2), ('*', 4, 3),
    ('4', 5, 0), ('5', 5, 1), ('6', 5, 2), ('-', 5, 3),
    ('1', 6, 0), ('2', 6, 1), ('3', 6, 2), ('+', 6, 3),
    ('', 7, 0), ('0', 7, 1), ('.', 7, 2), ('=', 7, 3),
 ]

 # 버튼 생성 및 배치
for text, row, col in button_values:
    if text == "C":
        button = tk.Button(root, text=text, padx=20, pady=20, command=clear)
    elif text == "=":
        button = tk.Button(root, text=text, padx=20, pady=20, command=calculate)
    elif text == "←":
        button = tk.Button(root, text=text, padx=20, pady=20, command=backSpace)
    elif text in "+-*/": #연산자 경우 추가
        button = tk.Button(root, text=text, padx=20, pady=20, command=lambda t=text: operator_click(t))
    elif text in "%": #연산자 경우 추가
        button = tk.Button(root, text=text, padx=20, pady=20, command=percent)
    elif text in ["1/χ"]: #연산자 경우 추가
        button = tk.Button(root, text=text, padx=20, pady=20, command=lambda t=text: operator_click(t))
    elif text in "χ²": #연산자 경우 추가
        button = tk.Button(root, text=text, padx=20, pady=20, command=lambda t=text: operator_click(t))
    elif text in "√χ": #연산자 경우 추가
        button = tk.Button(root, text=text, padx=20, pady=20, command=lambda t=text:operator_click(t))
    else:
        button = tk.Button(root, text=text, padx=20, pady=20, font=("default",12) ,command=lambda t=text: button_click(t))
    
    button.grid(row=row, column=col, padx=5, pady=5)



#today = datetime.date.today()
#populate_calendar(today.year, today.month)
#date_label = tk.Label(root, text=today.strftime("%B %Y"))
#date_label.pack()

 
 # 메인 루프 실행
root.mainloop()
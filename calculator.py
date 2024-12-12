import tkinter as tk
#import datetime
import re  #파이썬 정규표현식
from decimal import Decimal #정확한 십진수연산을 도와줌

# flag
new_calculation = False
operator_clicked = False
#'%'연산 위해 순차적 계산으로 변경 중
stored_value = 0 #저장된 값
current_operator = None #최근 연산자
percent_is = False


# 키보드 입력 처리
def keypress(event):
    global new_calculation,operator_clicked
    key = event.char

    valid_chars = "0123456789+-*/." # 유효 문자 정의

    if event.keysym == "BackSpace":  # event.char -> event.keysym()
        backSpace()
        return "break"
    elif event.keysym == "Return":  # Enter
        calculate()
        return "break"

    # 유효한 문자가 아니면 무시
    if not key or key not in valid_chars:
        return "break"

    # 유효한 문자(숫자, '.', 연산자)인 경우
    if key in "+-*/":
        # 연산자 처리
        operator_click(key)
       # operator_clicked = True
    else:
        
        button_click(key)
        #entry.insert(tk.END, key)

    return "break"


def button_click(number):
    global new_calculation, operator_clicked
    current = entry.get()

    if new_calculation:
        entry.delete(0, tk.END)
        entry2.delete("1.0", "end")
        entry.insert(0, str(number))
        new_calculation = False
        return "break"

    if operator_clicked:  # 마지막 문자가 연산자인 경우
        entry.delete(0, tk.END)  # Entry 리셋
        current=""
        
        
    entry.delete(0, tk.END)
    entry.insert(0, current + str(number))
    operator_clicked = False

    
def operator_click(operator):
    global new_calculation, operator_clicked
    global stored_value, current_operator, percent_is

    current = entry.get()
    current2 = entry2.get("1.0", "end").strip()
    print("current: ",current)
    print("current2: ",current2)
    print("percent_is: ",percent_is)
     
    if new_calculation:
        entry2.delete("1.0","end")
        entry2.insert("1.0", current + operator)
        new_calculation = False 
        operator_clicked = True
        print("newcal",new_calculation)
    
    if current:
        if percent_is:
            print("@@#####stored_value:",(stored_value))
            print("@@#####current_operator:",(current_operator))
            print("@@#####current:",(current))
            if current_operator is None:
                 result = eval(f"{current}")
            else:          
                result = eval(f"{stored_value}{current_operator}{current}")
            entry.delete(0, tk.END)
            entry.insert(0, result)
            entry2.delete("1.0","end")
            entry2.insert("end", f"{result}{operator}")
            percent_is = False
            print("percent_is",percent_is)
            current_operator = operator
            operator_clicked = True
            percent_is = False
            #reset_entry = True  # 다음 숫자 입력 시 entry를 초기화
            print("operator_clicked:",(operator_clicked))
            print("@!!current_operator:",(current_operator))
            return "break"
            

        if operator_clicked :         
            entry2.delete("end-2c", "end-1c")  # 연산자 두번입력 시  뒤에 누른 연산자로 바꾸기
            entry2.insert("end", f"{operator}")
            print(f"Operator replaced with: {operator}")

        else:
             full_expression = f"{current2} {current}"
             stored_value = eval(full_expression)
             print(f"Evaluated expression: {full_expression} = {stored_value}")
             entry2.delete("1.0","end")
             entry2.insert("end", f"{stored_value}{operator}")
             entry.delete(0, tk.END)
             entry.insert(0,stored_value)
            
        current_operator = operator
        operator_clicked = True
        percent_is = False
        #reset_entry = True  # 다음 숫자 입력 시 entry를 초기화
        print("operator_clicked:",(operator_clicked))
        print("@@@current_operator:",(current_operator))
    else:
        return

def percent():
    global current_operator  # 글로벌 변수 선언
    global percent_is, stored_value

    current = entry.get()  # 현재 입력 값
    current2 = entry2.get("1.0", "end-2c").strip()  # 계산식 전체
    #last_value = float(current2) if current2 else 0
    print(current)
    print(current2)
  #  print(last_value)

    if new_calculation:
        current_value = Decimal(current)
        percent_op = current_value * Decimal('0.01')
        result = f"{percent_op}"
        entry.delete(0, tk.END)
        entry.insert(0, percent_op)

    else:  
        # 현재 입력값을 숫자로 변환
        current_value = Decimal(current)
        last_value = Decimal(current2)

        # 연산자에 따른 퍼센트 계산
        if current_operator in "+-":
            percent_op = last_value * current_value * Decimal('0.01')
            #pattern = r"(\d+(\.\d+)?)"  # 숫자 패턴: 하나 이상의 숫자 + (선택적으로 '.' 뒤에 숫자들)
            # 정규표현식을 사용해 모든 숫자를 Decimal('...')로 감싸기
            result = f"{last_value}{current_operator}{percent_op}"
            entry.delete(0, tk.END)
            entry.insert(0, percent_op)
            percent_is = True


        elif current_operator in "*/":
            percent_op = current_value * Decimal('0.01')
            #pattern = r"(\d+(\.\d+)?)"
            result = f"{last_value}{current_operator}{percent_op}"
            entry.delete(0, tk.END)
            entry.insert(0, percent_op)
            percent_is = True

        else:
            entry.insert(0, "Error")
            print("123123Invalid operator for percent calculation.")
            return        

    entry2.delete("1.0", "end")
    entry2.insert("end", str(result))
    print(f"Percent calculated: {result}")
    
def reciprocal(): #역수계산
    global current_operator  # 글로벌 변수 선언
    global percent_is
    current = entry.get()  # 현재 입력 값
    current2 = entry2.get("1.0", "end-2c").strip()  # 계산식 전체
    #last_value = float(current2) if current2 else 0
    print(current)
    print(current2)
    try:
        num = float(current)  # 문자열을 숫자로 변환
        if num == 0:
            entry.delete(0, tk.END)
            entry.insert(0, "Error: Cannot divide by zero")  # 0으로 나누는 경우 처리
            return # 함수 종료

        reciprocal_val = 1 / num
        entry.delete(0, tk.END)  # 입력창 내용 지우기
        entry.insert(0, str(reciprocal_val)) # 역수 값을 입력창에 표시
        entry2.insert("end", f"1/{current} = {reciprocal_val}\n")  # 계산 과정과 결과 표시 수정
        

    except ValueError:
        entry.delete(0, tk.END)
        entry.insert(0, "Error: Invalid input")  # 유효하지 않은 입력 처리
    except ZeroDivisionError: # 추가적인 0으로 나누기 에러 처리
        entry.delete(0,tk.END)
        entry.insert(0,"Error : cannot divide by zero")

def sqr(x):
    return Decimal(x) ** 2

def pow():
    global current_operator, percent_is, new_calculation, operator_clicked, stored_value
    current = entry.get()  # 현재 입력 값
    current2 = entry2.get("1.0", "end-2c").strip()
    print("current:", current)
    print("current2:", current2)
    
    try:
        # 현재 입력값의 제곱 계산
        current_value = Decimal(current) ** 2
        # 계산 과정을 entry2에 기록 (sqr(값) 형식)
        last_value = "sqr(" + current + ")"
        entry2.delete("1.0", "end")
        if current_operator is None:
             entry2.insert("end", current2 + last_value)
        else:
            entry2.insert("end", current2 + current_operator +last_value)
        print("last_value:", last_value)
        result = eval(last_value, {"sqr": sqr, "Decimal": Decimal}, {})
        # 결과를 entry에 반영
        entry.delete(0, tk.END)
        entry.insert(0, current_value)

        # pow 연산 후 다음 연산을 바로 이어나갈 수 있도록 상태 초기화
        stored_value = current2
        new_calculation = False   # 새 계산 상태를 False로 하여 바로 다음 연산자 입력 가능
        operator_clicked = False  # 다음 연산자를 누를 때 정상적으로 작동하도록
        percent_is = True

    except Exception as e:
        entry.delete(0, tk.END)
        entry.insert(0, "Error")
        print("Error in pow calculation:", str(e))


def clear():
    global new_calculation,percent_is,operator_clicked,current_operator,stored_value
    entry.delete(0, tk.END)
    entry2.delete("1.0","end")
    new_calculation = False
    percent_is = False
    operator_clicked = False
    current_operator= None
    stored_value = 0 #저장된 값

def backSpace():
     # 현재 텍스트 가져오기
    current_text = entry.get()
   #current2 = entry2.get("1.0","end").strip()
    if current_text:  # 텍스트가 있을 경우
        # 마지막 글자를 제외한 텍스트로 업데이트
        entry.delete(0, tk.END)
        entry.insert(0, current_text[:-1])
        #entry2.delete("end-2c", "end-1c")  # Tkinter Text widget에서 마지막 문자 삭제

def calculate(event=None):
    global new_calculation, percent_is
    current = entry.get()
    current2 = entry2.get("1.0","end").strip()
    print(percent_is)

    if percent_is:
        expr = current2
        current = ""
    else:
        expr = current2 + current  

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
        percent_is = False
        print("newcal: ",new_calculation)
    except Exception:
        entry.delete(0, tk.END)
        entry.insert(0, "Error")
        new_calculation = True

    
 
 # GUI 초기화
root = tk.Tk()
root.title("Calculator")

entry = tk.Entry(root, width=35, borderwidth=5, font=("default",13))
entry.grid(row=1, column=0, columnspan=4, padx=10, pady=10)

entry2 = tk.Text(root, width=35,height=5, borderwidth=5)
entry2.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

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
        button = tk.Button(root, text=text, padx=20, pady=20, command=reciprocal)
    elif text in "χ²": #연산자 경우 추가
        button = tk.Button(root, text=text, padx=20, pady=20, command=pow)
    elif text in "√χ": #연산자 경우 추가
        button = tk.Button(root, text=text, padx=20, pady=20, command=lambda t=text:operator_click(t))
    else:
        button = tk.Button(root, text=text, padx=20, pady=20, font=("default",12) ,command=lambda t=text: button_click(t))
    
    button.grid(row=row, column=col, padx=5, pady=5)
 
 # 메인 루프 실행
root.mainloop()
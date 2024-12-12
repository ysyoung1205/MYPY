def pow():
    global current_operator, percent_is, new_calculation, operator_clicked, stored_value
    current = entry.get()  # 현재 입력 값
    current2 = entry2.get("1.0", "end").strip()
    print("current:", current)
    print("current2:", current2)
    
    try:
        # 현재 입력값의 제곱 계산
        current_value = Decimal(current) ** 2
        # 계산 과정을 entry2에 기록 (sqr(값) 형식)
        last_value = "sqr(" + current + ")"
        entry2.delete("1.0", "end")
        entry2.insert("end", current2 + last_value)
        print("last_value:", last_value)
        result = eval(last_value, {"sqr": sqr, "Decimal": Decimal}, {})
        # 결과를 entry에 반영
        entry.delete(0, tk.END)
        entry.insert(0, current_value)

        # pow 연산 후 다음 연산을 바로 이어나갈 수 있도록 상태 초기화
        stored_value = current_value
        new_calculation = False   # 새 계산 상태를 False로 하여 바로 다음 연산자 입력 가능
        operator_clicked = False  # 다음 연산자를 누를 때 정상적으로 작동하도록
        percent_is = True
    except Exception as e:
        entry.delete(0, tk.END)
        entry.insert(0, "Error")
        print("Error in pow calculation:", str(e))
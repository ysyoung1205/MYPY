def operator_click(operator):
    global new_calculation, operator_clicked
    global stored_value, current_operator

    current = entry.get()
    current2 = entry2.get("1.0", "end").strip()
    
    if new_calculation:
        entry2.delete("1.0","end")
        new_calculation = False 
    
    if current:
        if operator_clicked :
            stored_value = current2 + current
            print(stored_value)
            entry2.delete("end-2c", "end-1c")  
            entry2.insert("end", f"{operator}")
            print(f"Operator replaced with: {operator}")

        else:
            try:
                entry2.insert("end", current+ f"{operator}")
                stored_value = current2 + current
                print("stored_value",stored_value)
            except ValueError:
                entry.delete(0, tk.END)
                entry.insert(0, "Error")
                print("Invalid input for operator")
                return
        
        current_operator = operator
        operator_clicked = True

        print(operator_clicked)
    else:
        return
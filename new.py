from tkinter import *

root = Tk() # GUI 생성 
root.title("tkinter_practice") #상단의 타이틀 지정
root.geometry("640x640") # 크기 설정 (640x640) 

btn1 = Button(root, text = "기본버튼")  #root로 지정한 윈도우에 button 생성
btn1.pack() # 윈도우상에 상대 위치로 위젯을 배치

btn2 = Button(root, width = 10 , height = 10 , text="크기설정버튼")
btn2.pack()

root.mainloop() # GUI가 보이고 종료될때까지 실행함
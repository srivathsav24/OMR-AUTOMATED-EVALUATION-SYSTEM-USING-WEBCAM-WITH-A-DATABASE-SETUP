
from tkinter import *
import OMR_Main

root=Tk()
root.title(" OMR EVALUATING APPLICATION ")
root.geometry("800x700")

def home_page():
    global main_frame
    main_frame=Frame(root,width=800,height=700,bg="black")
    main_frame.pack(fill="both",expand=1)
    l1=Label(main_frame,text=" OMR AUTOMATED EVALUATION SYSTEM ",bg="black",fg="white",font=("times new roman",20,"bold"))
    l1.grid(row=0,column=0,padx=100,pady=150)
    global e
    e=Entry(main_frame,width=90)
    e.grid(row=1,column=0,padx=90,pady=30)
    b=Button(main_frame,text=" CREATE SCANNER  ",command=OMR_Main.fun,width=20,bg="green",fg="white",font=("times new roman",20,"bold"))
    b.grid(row=2,padx=90)


def data_page():
    global fr2
    fr2=Frame(root,width=800,height=700,bg="black")
    fr2.pack(fill="both",expand=1)
    my_label=Label(fr2,text="DATABASE",bg="black",fg="white",font=("book antique",30,"bold"))
    my_label.pack()


def data_fun():
    main_frame.pack_forget()
    data_page()  
    

def home_action():
    fr2.pack_forget()
    main_frame.pack_forget()
    home_page()

home_page()


my_menu=Menu(root)
root.config(menu=my_menu)
home=Menu(my_menu)
my_menu.add_cascade(label=" MENU ",menu=home)
home.add_command(label=" HOME ",command=home_action)
home.add_separator()
home.add_command(label=" DATABASE ",command=data_fun)


root.mainloop()
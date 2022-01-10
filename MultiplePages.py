from tkinter import *
import pandas as pd
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import runpy

class FirstPage(Frame):
    def __init__(self,parent,controller):
        Frame.__init__(self,parent)

        image = Image.open("inputs/BG3.jpg")
        photo = ImageTk.PhotoImage(image)
        label = Label(self,image=photo)
        label.image = photo
        label.place(x=0,y=0)

        border = LabelFrame(self,text="Login",bg="ivory",bd=10,font="comicsansms 25 bold")
        border.pack(fill="both", expand="yes",padx=100,pady=100)

        user = Label(border, text="Username", bg="ivory",font="comicsansms 15 bold")
        user.place(x=150,y=200)
        userval = StringVar()
        userEntry = Entry(border, textvariable=userval,width=50,bd=5)
        userEntry.place(x=300,y=200)

        pwd = Label(border, text="Password", bg="ivory", font="comicsansms 15 bold")
        pwd.place(x=150,y=300)
        pwdval = StringVar()
        pwdentry = Entry(border, textvariable=pwdval,show="*",width=50,bd=5)
        pwdentry.place(x=300,y=300)

        def Verify():
            try:
                with open("LoginList.txt", "r") as f:
                    info = f.readlines()
                    chk = 0
                    for line in info:
                        u, p = line.split(",")

                        if u.strip() == userEntry.get() and p.strip() == pwdentry.get():
                            controller.show_frame(SecondPage)
                            chk = 1
                            break
                    if (chk == 0):
                        messagebox.showinfo("Error", "Please provide correct username or password!!")
            except:
                messagebox.showinfo("Error", "Please provide correct username or password!!")

        B1 = Button(border, text="Submit",bg="light green" ,font="Arial 17 bold", relief=RAISED,
                    command=Verify)
        B1.place(x=350, y=400)

        def register():
            window =Tk()
            window.title("Register")
            window.resizable(0,0)
            window.configure(bg="light yellow")


            L1 = Label(window, text="Username", bg="light yellow", font="comicsansms 15 bold")
            L1.place(x=10, y=10)
            L1val = StringVar()
            L1Entry = Entry(window, textvariable=L1val, width=30, bd=5)
            L1Entry.place(x=200, y=10)

            L2 = Label(window, text="Password", bg="light yellow", font="comicsansms 15 bold")
            L2.place(x=10, y=60)
            L2val = StringVar()
            L2Entry = Entry(window, textvariable=L2val, show="*",width=30, bd=5)
            L2Entry.place(x=200, y=60)

            L3 = Label(window, text="Confirm Password", bg="light yellow", font="comicsansms 15 bold")
            L3.place(x=10, y=110)
            L3val = StringVar()
            L3Entry = Entry(window, textvariable=L3val, show="*",width=30, bd=5)
            L3Entry.place(x=200, y=110)

            def check():
                if L1Entry.get()!="" and L2Entry.get()!="" and L3Entry.get()!="":
                    if L2Entry.get() == L3Entry.get():
                        path = "SignIn_Rec.xlsx"
                        df1 = pd.read_excel(path)
                        seriesA = df1['Username']
                        seriesB = df1['Password']
                        A = pd.Series(L1Entry.get())
                        B = pd.Series(L2Entry.get())
                        seriesA = seriesA.append(A)
                        seriesB = seriesB.append(B)
                        df2 = pd.DataFrame({"Username": seriesA, "Password": seriesB})
                        df2.to_excel(path, index=False)

                        with open("LoginList.txt","a") as f:
                            f.write(L1Entry.get()+","+L2Entry.get()+"\n")

                        L1Entry.delete(0, END)
                        L2Entry.delete(0, END)
                        L3Entry.delete(0,END)

                        messagebox.showinfo("Welcome","You are registered successfully!!")
                    else:
                        messagebox.showinfo("Error","Your password didn't get matched!!")
                else:
                    messagebox.showinfo("Error","Please fill the complete field!!")

            b1 = Button(window,text="Sign In",bg="Yellow",relief=RAISED,font="comicsansms 12 bold",command=check)
            b1.place(x=200,y=150)

            window.geometry("470x220")
            window.mainloop()

        B2 = Button(border, text="Register", font="Arial 15 bold",bg="light sky blue" ,relief=SUNKEN,
                    command=register)
        B2.place(x=590, y=30)




class SecondPage(Frame):
    def __init__(self,parent,controller):
        Frame.__init__(self,parent)
        image = Image.open("inputs/BG5.png")
        photo = ImageTk.PhotoImage(image)
        label = Label(self, image=photo)
        label.image = photo
        label.place(x=0, y=0)

        B1 = Button(self, text="Back", font="Arial 15 bold", bg="light goldenrod",
                    relief=SUNKEN,command=lambda: controller.show_frame(FirstPage))
        B1.place(x=100, y=700)


        B2 = Button(self, text="Start", font="Arial 23 bold",bg="goldenrod", command=lambda: controller.show_frame(ThirdPage))
        B2.place(x=680, y=450)

class ThirdPage(Frame):
    def __init__(self,parent,controller):
        Frame.__init__(self,parent)
        image = Image.open("inputs/appPage2.png")
        photo = ImageTk.PhotoImage(image)
        label = Label(self, image=photo)
        label.image = photo
        label.place(x=0, y=0)

        B1 = Button(self, text="Home", font="Arial 18 bold",bg="light goldenrod",relief=SUNKEN, command=lambda: controller.show_frame(FirstPage))
        B1.place(x=850, y=700)


        def virtual_paint():
            path="Project4-VirtualPainter.py"
            runpy.run_path(path_name=path)

        B3 = Button(self,text="Virtual_Paint",font="Arial 15 bold",bg="light green",relief=RAISED,command=virtual_paint)
        B3.place(x=90,y=320)

        def virtual_keyboard():
            path="Project6-Keyboard.py"
            runpy.run_path(path_name=path)

        B3 = Button(self,text="Virtual_Keyboard",font="Arial 15 bold",bg="light green",relief=RAISED,command=virtual_keyboard)
        B3.place(x=70,y=570)

        def virtual_mouse():
            path="Project5-Virtual_Mouse.py"
            runpy.run_path(path_name=path)

        B3 = Button(self,text="Virtual_Mouse",font="Arial 15 bold",bg="light green",relief=RAISED,command=virtual_mouse)
        B3.place(x=320,y=320)

        def virtual_volume():
            path="Project1-VolumeControl.py"
            runpy.run_path(path_name=path)

        B3 = Button(self,text="Virtual_Volume_Control",font="Arial 15 bold",bg="light green",relief=RAISED,command=virtual_volume)
        B3.place(x=340,y=570)
class Application(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self,*args, **kwargs)

        # TODO: Creating a Window

        window = Frame(self)
        window.pack()

        window.grid_rowconfigure(0,minsize=800)
        window.grid_columnconfigure(0,minsize=1000)

        self.frames = {}
        for F in (FirstPage,SecondPage,ThirdPage):
            frame = F(window,self)
            self.frames[F] = frame
            frame.grid(row = 0, column = 0, sticky="nsew")

        self.show_frame(FirstPage)

    def show_frame(self,page):
        frame = self.frames[page]
        frame.tkraise()

app = Application()
app.maxsize(1000,800)
app.mainloop()
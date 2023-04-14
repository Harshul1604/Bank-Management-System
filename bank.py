from tkinter import *
from PIL import Image,ImageTk
from tkinter.ttk import Combobox
from datetime import datetime
from tkinter import messagebox
import sqlite3
con=sqlite3.connect(database="bank.sqlite")
cur=con.cursor()
table1="create table accounts(account_no integer primary key autoincrement,account_name text,account_pass text,account_email text,account_mob text,account_type text,account_bal float,account_opendate texr)"
table2="create table txn(txn_account_no int,txn_amt float,txn_update_bal float,txn_date text,txn_type text)"
try:
    cur.execute(table1)
    cur.execute(table2)
    print("Table created")
except:
    print("Something went wrong,Table already exists")
con.commit()
con.close()

win=Tk()
win.state("zoomed")
win.configure(bg="powder blue")


label_title= Label(win,text="Banking Automation", bg="powder blue" ,font=('Arial' ,60,'bold','underline'))
label_title.place(relx=.25,rely=.025)

img=Image.open("logo2.png").resize((260,140))
imgtk= ImageTk.PhotoImage(img,master=win)

lbl_logo=Label(win,image=imgtk)
lbl_logo.place(x=0,y=0)


def login_screen():
    frm=Frame(win)
    frm.configure(bg="pink")
    frm.place(relx=0,rely=.2,relwidth=1,relheight=.9)
    
    def newuser():
        frm.destroy()
        newuser_screen()
        
    def forget():
        frm.destroy()
        forget_screen()
        
    def login_db():
        acn=e_acn.get()
        pwd=e_pass.get()
        if(acn=="" or pwd==""):
            messagebox.showwarning("Login","Please fill both fields")
        else:
            con=sqlite3.connect(database="bank.sqlite")
            cur=con.cursor()
            cur.execute("select * from accounts where account_no=? and account_pass=?",(acn,pwd))
            global tup
            tup=cur.fetchone()
            if(tup==None):
                messagebox.showerror("login","Invalid ACN or PASS")
            else:
                frm.destroy()
                welcome_screen()
                        
    def reset_db():
        e_acn.delete(0,"end")
        e_pass.delete(0,"end")
        e_acn.focus()
        
               
        
    label_acn= Label(frm,text="Account No", bg="pink" ,font=('Arial' ,20,'bold',))
    label_acn.place(relx=.3,rely=.1)
    
    e_acn=Entry(frm,font=('Arial',20,'bold'),bd=5)
    e_acn.place(relx=.45,rely=.1)
    e_acn.focus()
    
    label_pass= Label(frm,text="Password", bg="pink" ,font=('Arial' ,20,'bold',))
    label_pass.place(relx=.3,rely=.25)
    
    e_pass=Entry(frm,font=('Arial',20,'bold'),bd=5,show="*")
    e_pass.place(relx=.45,rely=.25)
    
    btn_login=Button(frm,text="Login",command=login_db,font=('Arial',20,'bold'),bd=5,bg="powder blue")
    btn_login.place(relx=.4,rely=.4)
    btn_reset=Button(frm,text="Reset",command=reset_db,font=('Arial',20,'bold'),bd=5,bg="powder blue")
    btn_reset.place(relx=.49,rely=.4)
    btn_fb=Button(frm,text="Forget password",font=('Arial',20,'bold'),bd=5,bg="powder blue",command=forget)
    btn_fb.place(relx=.4,rely=.55)
    btn_new=Button(frm,text="Open New Account",font=('Arial',20,'bold'),bd=5,bg="powder blue",command=newuser)
    btn_new.place(relx=.4,rely=.7)
    
def newuser_screen():
    frm=Frame(win)
    frm.configure(bg="pink")
    frm.place(relx=0,rely=.2,relwidth=1,relheight=.9)
    
    def back():
        frm.destroy()
        login_screen()
        
    def openacn_db():
        name=e_name.get()
        pwd=e_pass.get()
        email=e_email.get()
        mob=e_mob.get()
        acn_type=cb_type.get()
        if(acn_type=="Saving"):
            bal=1000
        else:
            bal=10000       
        opendate=str(datetime.now().date())
        
        con=sqlite3.connect(database="bank.sqlite")
        cur=con.cursor()
        cur.execute("insert into accounts(account_name,account_pass,account_email,account_mob,account_type,account_bal,account_opendate) values(?,?,?,?,?,?,?)",(name,pwd,email,mob,acn_type,bal,opendate))
        con.commit()
        con.close()
        
        con=sqlite3.connect(database="bank.sqlite")
        cur=con.cursor()
        cur.execute("select max(account_no) from accounts")
        tup=cur.fetchone()
        con.close()
        messagebox.showinfo("Success",f"Account opened with acn no: {tup[0]}")
        frm.destroy()
        login_screen()
        
        
    btn_back=Button(frm,text="Back",font=('Arial',20,'bold'),bd=5,bg="powder blue",command=back)
    btn_back.place(relx=0,rely=0)
    
    label_name= Label(frm,text="Name", bg="pink" ,font=('Arial' ,20,'bold',))
    label_name.place(relx=.3,rely=.05)
    
    e_name=Entry(frm,font=('Arial',20,'bold'),bd=5)
    e_name.place(relx=.45,rely=.05)
    e_name.focus()
    
    label_pass= Label(frm,text="Password", bg="pink" ,font=('Arial' ,20,'bold',))
    label_pass.place(relx=.3,rely=.15)
    
    e_pass=Entry(frm,font=('Arial',20,'bold'),bd=5)
    e_pass.place(relx=.45,rely=.15)
    
    label_email= Label(frm,text="Email", bg="pink" ,font=('Arial' ,20,'bold',))
    label_email.place(relx=.3,rely=.25)
    
    e_email=Entry(frm,font=('Arial',20,'bold'),bd=5)
    e_email.place(relx=.45,rely=.25)
    
    label_mob= Label(frm,text="Mob No.", bg="pink" ,font=('Arial' ,20,'bold',))
    label_mob.place(relx=.3,rely=.35)
    
    e_mob=Entry(frm,font=('Arial',20,'bold'),bd=5)
    e_mob.place(relx=.45,rely=.35)
    
    label_type= Label(frm,text="Acn Type", bg="pink" ,font=('Arial' ,20,'bold',))
    label_type.place(relx=.3,rely=.45)
    
    cb_type= Combobox(frm,values=['Saving','Current'],font=('Arial' ,20,'bold',))
    cb_type.current(0)
    cb_type.place(relx=.45,rely=.45)
    
     
    btn_open=Button(frm,text="Open",command=openacn_db,font=('Arial',20,'bold'),bd=5,bg="powder blue")
    btn_open.place(relx=.4,rely=.6)
    btn_reset=Button(frm,text="Reset",font=('Arial',20,'bold'),bd=5,bg="powder blue")
    btn_reset.place(relx=.49,rely=.6)
                                                                                              
def forget_screen():
    frm=Frame(win)
    frm.configure(bg="pink")
    frm.place(relx=0,rely=.2,relwidth=1,relheight=.9)
    
    def back():
        frm.destroy()
        login_screen()
        
    def get_db():
        acn=e_acn.get()
        mob=e_mob.get()
        email=e_email.get()
        
        if(acn=="" or email=="" or mob==""):
            messagebox.showwarning("Warning","Please fill all fields")
            return
        else:
            con=sqlite3.connect(database="bank.sqlite")
            cur=con.cursor()
            cur.execute("select account_pass from accounts where account_no=? and account_email=? and account_mob=?",(acn,email,mob))
            tup=cur.fetchone()
            if(tup==None):
                messagebox.showwarning("Forgot","Invalid details")
            else:
                messagebox.showinfo("forgot",f"Your password is: {tup[0]}")        
    
    btn_back=Button(frm,text="Back",font=('Arial',20,'bold'),bd=5,bg="powder blue",command=back)
    btn_back.place(relx=0,rely=0)
    
    label_acn= Label(frm,text="Acn No.", bg="pink" ,font=('Arial' ,20,'bold',))
    label_acn.place(relx=.3,rely=.05)
    
    e_acn=Entry(frm,font=('Arial',20,'bold'),bd=5)
    e_acn.place(relx=.45,rely=.05)
    e_acn.focus()
    
    label_email= Label(frm,text="Email", bg="pink" ,font=('Arial' ,20,'bold',))
    label_email.place(relx=.3,rely=.2)
    
    e_email=Entry(frm,font=('Arial',20,'bold'),bd=5)
    e_email.place(relx=.45,rely=.2)
    
    label_mob= Label(frm,text="Mob No.", bg="pink" ,font=('Arial' ,20,'bold',))
    label_mob.place(relx=.3,rely=.35)
    
    e_mob=Entry(frm,font=('Arial',20,'bold'),bd=5)
    e_mob.place(relx=.45,rely=.35) 
     
    btn_get=Button(frm,text="Get",command=get_db,font=('Arial',20,'bold'),bd=5,bg="powder blue")
    btn_get.place(relx=.4,rely=.5)
    btn_reset=Button(frm,text="Reset",font=('Arial',20,'bold'),bd=5,bg="powder blue")
    btn_reset.place(relx=.49,rely=.5)
                                                                                              
def welcome_screen():
    frm=Frame(win)
    frm.configure(bg="pink")
    frm.place(relx=0,rely=.2,relwidth=1,relheight=.9)
     
    def logout_db():
        frm.destroy()
        login_screen()
        
    def checkbal():
        ifrm=Frame(frm,highlightbackground='brown',highlightthickness=5,highlightcolor='brown')
        ifrm.configure(bg='white')
        ifrm.place(relx=.25,rely=.2,relwidth=.6,relheight=.6)
        label_page.configure(text="Check balance page")
        
        
        
        
        label_acn= Label(ifrm,text=f"Holder Name:  {tup[1]}", bg="white" ,font=('Arial' ,20,'bold'),fg='red')
        label_acn.place(relx=.3,rely=.1)
        
        label_bal= Label(ifrm,text=f"Account bal:{tup[6]}", bg="white" ,font=('Arial' ,20,'bold'),fg='red')
        label_bal.place(relx=.3,rely=.3)
    
        label_date= Label(frm,text=f" Openning date:{tup[7]}", bg="white" ,font=('Arial' ,20,'bold'),fg='red')
        label_date.place(relx=.42,rely=.5)
        
    def deposit():
        ifrm=Frame(frm,highlightbackground='brown',highlightthickness=5,highlightcolor='brown')
        ifrm.configure(bg='white')
        ifrm.place(relx=.25,rely=.2,relwidth=.6,relheight=.6)
        label_page.configure(text="Deposit page") 
        
        def deposite_db():
            amt=float(e_amt.get())
            acn=tup[0]
            txn_type="CREDIT"
            dt=str(datetime.now())
            
            con=sqlite3.connect(database="bank.sqlite")
            cur=con.cursor()
            cur.execute("select account_bal from accounts where account_no=?",(acn,))
            bal=cur.fetchone()[0]
            con.close()
            
            
            con=sqlite3.connect(database="bank.sqlite")
            cur=con.cursor()
            cur.execute("insert into txn values(?,?,?,?,?)",(acn,amt,bal+amt,dt,txn_type))
            cur.execute("update accounts set account_bal=account_bal+? where account_no=?",(amt,acn))
            con.commit()
            con.close()
            
            messagebox.showinfo("Deposit","Ammount deposited")
            
            
        
        label_amt= Label(ifrm,text="Enter amount: ", bg="white" ,font=('Arial' ,20,'bold'),fg='red')
        label_amt.place(relx=0.2,rely=0.2)
        
        e_amt=Entry(ifrm,font=('Arial',20,'bold'),bd=5)
        e_amt.place(relx=.45,rely=.2)
        
          
        btn_dep=Button(ifrm,text="Deposit",command=deposite_db,font=('Arial',20,'bold'),bd=5,bg="powder blue")
        btn_dep.place(relx=0.5,rely=0.5)
    
        
    def withdraw():
        
        def withdraw_db():
            amt=float(e_amt.get())
            acn=tup[0]
            txn_type="DEBIT"
            dt=str(datetime.now())
            
            con=sqlite3.connect(database="bank.sqlite")
            cur=con.cursor()
            cur.execute("select account_bal from accounts where account_no=?",(acn,))
            bal=cur.fetchone()[0]
            con.close()
            
            if(bal>=amt):
                con=sqlite3.connect(database="bank.sqlite")
                cur=con.cursor()
                cur.execute("insert into txn values(?,?,?,?,?)",(acn,amt,bal+amt,dt,txn_type))
                cur.execute("update accounts set account_bal=account_bal-? where account_no=?",(amt,acn))
                con.commit()
                con.close()
            
                messagebox.showinfo("Withdraw","Ammount Withdrawed")
            else:
                messagebox.showwarning("Withdraw","Insufficient bal")
                    
                 
        ifrm=Frame(frm,highlightbackground='brown',highlightthickness=5,highlightcolor='brown')
        ifrm.configure(bg='white')
        ifrm.place(relx=.25,rely=.2,relwidth=.6,relheight=.6)
        label_page.configure(text="Withdraw page") 
        
        
        label_amt= Label(ifrm,text="Enter amount: ", bg="white" ,font=('Arial' ,20,'bold'),fg='red')
        label_amt.place(relx=0.2,rely=0.2)
        
        e_amt=Entry(ifrm,font=('Arial',20,'bold'),bd=5)
        e_amt.place(relx=.45,rely=.2)
        
          
        btn_with=Button(ifrm,text="Withdraw",command=withdraw_db,font=('Arial',20,'bold'),bd=5,bg="powder blue")
        btn_with.place(relx=0.5,rely=0.5) 
    
    def transfer():
                 
        ifrm=Frame(frm,highlightbackground='brown',highlightthickness=5,highlightcolor='brown')
        ifrm.configure(bg='white')
        ifrm.place(relx=.25,rely=.2,relwidth=.6,relheight=.6)
        label_page.configure(text="Transfer page") 
        
        
        label_amt= Label(ifrm,text="Enter amount: ", bg="white" ,font=('Arial' ,20,'bold'),fg='red')
        label_amt.place(relx=0.2,rely=0.2)
        
        e_amt=Entry(ifrm,font=('Arial',20,'bold'),bd=5)
        e_amt.place(relx=.45,rely=.2)
        
        
        label_to= Label(ifrm,text="To Acc No: ", bg="white" ,font=('Arial' ,20,'bold'),fg='red')
        label_to.place(relx=0.2,rely=0.4)
        
        e_to=Entry(ifrm,font=('Arial',20,'bold'),bd=5)
        e_to.place(relx=.45,rely=.4)
        
          
        btn_tran=Button(ifrm,text="Transfer",font=('Arial',20,'bold'),bd=5,bg="powder blue")
        btn_tran.place(relx=0.5,rely=0.6)  
                 
    def update():
                 
        ifrm=Frame(frm,highlightbackground='brown',highlightthickness=5,highlightcolor='brown')
        ifrm.configure(bg='white')
        ifrm.place(relx=.25,rely=.2,relwidth=.6,relheight=.6)
        label_page.configure(text="Transfer page") 
        
        
        label_name= Label(ifrm,text="Name: ", bg="white" ,font=('Arial' ,15,'bold'),fg='red')
        label_name.place(relx=0.05,rely=0.2)
        
        e_name=Entry(ifrm,font=('Arial',15,'bold'),bd=5)
        e_name.place(relx=.15,rely=.2)
        
        label_pass= Label(ifrm,text="Pass: ", bg="white" ,font=('Arial' ,15,'bold'),fg='red')
        label_pass.place(relx=0.53,rely=0.2)
        
        e_pass=Entry(ifrm,font=('Arial',15,'bold'),bd=5)
        e_pass.place(relx=.62,rely=.2)
        
        label_email= Label(ifrm,text="email: ", bg="white" ,font=('Arial' ,15,'bold'),fg='red')
        label_email.place(relx=0.05,rely=0.4)
        
        e_email=Entry(ifrm,font=('Arial',15,'bold'),bd=5)
        e_email.place(relx=.15,rely=.4)
        
        label_mob= Label(ifrm,text="Mob: ", bg="white" ,font=('Arial' ,15,'bold'),fg='red')
        label_mob.place(relx=0.53,rely=0.4)
        
        e_mob=Entry(ifrm,font=('Arial',15,'bold'),bd=5)
        e_mob.place(relx=.62,rely=.4)
        
        btn_update=Button(ifrm,text="Update",font=('Arial',20,'bold'),bd=5,bg="powder blue")
        btn_update.place(relx=0.4,rely=0.6) 
            
    
    btn_logout=Button(frm,text="Logout",font=('Arial',20,'bold'),bd=5,bg="powder blue",command=logout_db)
    btn_logout.place(relx=.91,rely=0)
     
    label_well= Label(frm,text=f"Welcome,{tup[1]}", bg="pink" ,font=('Arial' ,20,'bold'),fg='green')
    label_well.place(relx=0,rely=0)
    
    label_page= Label(frm,text= "Home page", bg="pink" ,font=('Arial' ,30,'bold','underline'),fg='blue',)
    label_page.place(relx=0.45,rely=0)
    
    btn_checkbal=Button(frm,text="Check balance",width=12,command=checkbal,font=('Arial',20,'bold'),bd=5,bg="powder blue")
    btn_checkbal.place(relx=0,rely=0.1)
    
    btn_deposit=Button(frm,text="Deposit Cash",width=12,command=deposit,font=('Arial',20,'bold'),bd=5,bg="powder blue")
    btn_deposit.place(relx=0,rely=.2)
    
    btn_withdraw=Button(frm,text="Withdraw Cash",width=12,command=withdraw,font=('Arial',20,'bold'),bd=5,bg="powder blue")
    btn_withdraw.place(relx=0,rely=.3)
    
    btn_transfer=Button(frm,text="Transfer",width=12,command=transfer,font=('Arial',20,'bold'),bd=5,bg="powder blue")
    btn_transfer.place(relx=0,rely=.4)
    
    btn_update=Button(frm,text="Update Profile",width=12,command=update,font=('Arial',20,'bold'),bd=5,bg="powder blue")
    btn_update.place(relx=0,rely=.5)
    
    btn_history=Button(frm,text="Txn History",width=12,font=('Arial',20,'bold'),bd=5,bg="powder blue")
    btn_history.place(relx=0,rely=.6)
    
    
    
    
     
    
           
           
       
login_screen()    

win.mainloop()




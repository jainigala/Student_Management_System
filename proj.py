from tkinter import *
from tkinter import messagebox
from tkinter import scrolledtext
import cx_Oracle
import requests
import bs4
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np


root1 =Tk()
root1.overrideredirect(True)
root1.geometry("1200x800+150+30")
res=requests.get("https://www.brainyquote.com/quotes_of_the_day.html")
soup=bs4.BeautifulSoup(res.text,'lxml')
quote=soup.find('img',{"class":"p-qotd"})
pic_url="https://www.brainyquote.com" + quote['data-img-url']
r=requests.get(pic_url)
with open("quote.jpg",'wb') as f:
	f.write(r.content)
img=Image.open('quote.jpg')
img.save('quote.png')       

img=PhotoImage(file='quote.png')
logo=Label(root1,image=img,height=500,width=1000)
logo.place(x=100,y=50)

res=requests.get("https://ipinfo.io/")
data=res.json()
city=data['city']
if city=='Ghatkopar':
	city='Mumbai'
reg=data['region']
        
logo1=Label(root1,text=((city),",",(reg)))
logo1.place(x=570,y=650)
      
a1="http://api.openweathermap.org/data/2.5/weather?units=metric"
a2="&q="+city
a3="&appid=c6e315d09197cec231495138183954bd"
api_address=a1+a2+a3
res1=requests.get(api_address)
wdata=requests.get(api_address).json()
main=wdata['main']
temp=main['temp']
        
logo2=Label(root1,text=(temp ,'\u00b0'))
logo2.place(x=630,y=700)
root1.after(7000, root1.destroy)
root1.configure(background='ghost white')
root1.mainloop()


root=Tk()
root.title("S.M.S")
root.geometry("400x400+200+200")
root.configure(background='ghost white')

def f1():
	adSt.deiconify()
	root.withdraw()
def f3():
	viSt.deiconify()
	root.withdraw()
	con=None
	cursor=None
	try:
		con=cx_Oracle.connect("system/abc123")
		cursor=con.cursor()
		sql="select * from student"
		cursor.execute(sql)
		data=cursor.fetchall()
		msg=''
		for d in data:
			msg=msg + "RNo: "+str(d[0]) +" Name: "+ str(d[1]) + " Marks: "+str(d[2])+"\n"

		stData.insert(INSERT , msg)

	except cx_Oracle.DatabaseError as e:
		print("Select issue ",e)
	finally:
		if cursor is not None:
			cursor.close()
		if con is not None:
			con.close()
		
def f6():
	upSt.deiconify()
	root.withdraw()

def f9():
	delSt.deiconify()
	root.withdraw()


def f12():
	Name=[]
	Marks=[]

	con=None
	cursor=None
	try:
		con=cx_Oracle.connect("system/abc123")
		cursor=con.cursor()
		sql="select * from student"
		cursor.execute(sql)
		data=cursor.fetchall()

		for d in data:
			tp=list(d)
			Name.append(tp[1])
			Marks.append(tp[2])
	
		plt.bar(Name,Marks,width=0.25,label='marks')
		plt.title("Exam score",fontsize=20)
		plt.xlabel("name",fontsize=10)
		plt.ylabel("marks",fontsize=10)
		plt.legend()
		plt.grid()
		plt.show()
		
	except cx_Oracle.DatabaseError as e:
		print("Select issue ",e)
	finally:
		if cursor is not None:
			cursor.close()
		if con is not None:
			con.close()
	

	



btnAdd=Button(root,text="Add",background='linen',font=('arial',16,'bold'),width=10,command=f1)
btnView=Button(root,text="View",background='linen',font=('arial',16,'bold'),width=10,command=f3)
btnUpdate=Button(root,text="Update",background='linen',font=('arial',16,'bold'),width=10 ,command=f6)
btnDelete=Button(root,text="Delete",background='linen',font=('arial',16,'bold'),width=10 ,command=f9 )
btnGraph=Button(root,text="Graph",background='linen',font=('arial',16,'bold'),width=10 , command=f12 )


btnAdd.pack(pady=10)
btnView.pack(pady=10)
btnUpdate.pack(pady=10)
btnDelete.pack(pady=10)
btnGraph.pack(pady=10)

adSt=Toplevel(root)
adSt.title("Add Student")
adSt.geometry("400x400+200+200")
adSt.configure(background='ghost white')
adSt.withdraw()


def f2():
	root.deiconify()
	adSt.withdraw()
	entAddRno.delete(0,END)
	entAddName.delete(0,END)
	entAddMarks.delete(0,END)


def f5():
	con=None
	cursor=None
	try:
		con=cx_Oracle.connect("system/abc123")
		srno=entAddRno.get()
		if srno.isdigit() and int(srno)>0:
			rno=int(srno)
		else:
			messagebox.showerror("mistake","incorrect rno")
			entAddRno.delete(0,END)
			entAddRno.focus()
			return

		sname=(entAddName.get())
		if sname.isalpha():
			name=sname
		else:
			messagebox.showerror("Mistake","incorrect name")
			entAddName.delete(0,END)
			entAddName.focus()
			return

		smarks=entAddMarks.get()
		if smarks.isdigit() and int(smarks)<100:
			marks=int(smarks)
		else:
			messagebox.showerror("mistake","incorrect marks")
			entAddMarks.delete(0,END)
			entAddMarks.focus()
			return

		cursor=con.cursor()
		sql="insert into student values('%d','%s','%d')"
		args=(rno,name,marks)
		cursor.execute(sql % args)
		con.commit()
		msg=str(cursor.rowcount)+"rows inserted"
		messagebox.showinfo("Success",msg)
			
	except cx_Oracle.DatabaseError as e:
		con.rollback()
		messagebox.showerror("Failure",e)
	finally:
		if cursor is not None:
			cursor.close()
		if con is not None:
			con.close()
		
		
lblAddRno=Label(adSt,text="ENTER ROLL NO ")
lblAddName=Label(adSt,text="ENTER NAME ")
lblAddMarks=Label(adSt,text="ENTER MARKS ")
entAddRno=Entry(adSt,bd=5)
entAddName=Entry(adSt,bd=5)
entAddMarks=Entry(adSt,bd=5)
btnAddSave=Button(adSt,background='linen',font=('arial',12,'bold'),text="SAVE",command=f5)
btnAddBack=Button(adSt,background='linen',font=('arial',12,'bold'),text="BACK",command=f2)

lblAddRno.pack(pady=10)
entAddRno.pack(pady=10)
lblAddName.pack(pady=10)
entAddName.pack(pady=10)
lblAddMarks.pack(pady=10)
entAddMarks.pack(pady=10)
btnAddSave.pack(pady=10)
btnAddBack.pack(pady=10)

def f4():
	root.deiconify()
	viSt.withdraw()
	stData.delete('1.0',END)


viSt=Toplevel(root)
viSt.title("View Student")
viSt.geometry("400x400+200+200")
viSt.configure(background='ghost white')
viSt.withdraw()

stData=scrolledtext.ScrolledText(viSt,width=30,height=5)
btnViewBack=Button(viSt,background='linen',font=('arial',12,'bold'),text="BACK",command=f4)

stData.pack(pady=10)
btnViewBack.pack(pady=10)


def f7():
	root.deiconify()
	upSt.withdraw()
	entUpRno.delete(0,END)
	entUpName.delete(0,END)
	entUpMarks.delete(0,END)

def f8():
	con=None
	cursor=None
	try:
		con=cx_Oracle.connect("system/abc123")
		srno=entUpRno.get()
		if srno.isdigit() and int(srno)>0:
			rno=int(srno)
		else:
			messagebox.showerror("mistake","incorrect rno")
			entUpRno.delete(0,END)
			entUpRno.focus()
			return
		sname=(entUpName.get())
		if sname.isalpha():
			name=sname
		else:
			messagebox.showerror("Mistake","incorrect name")
			entUpName.delete(0,END)
			entUpName.focus()
			return
		smarks=entUpMarks.get()
		if smarks.isdigit() and int(smarks)<100:
			marks=int(smarks)
		else:
			messagebox.showerror("mistake","incorrect marks")
			entUpMarks.delete(0,END)
			entUpMarks.focus()
			return


		cursor=con.cursor()
		sql="update student set name='%s', marks='%d' where rno='%d' "
		args=(name,marks,rno)
		cursor.execute(sql % args)
		con.commit()
		msg=str(cursor.rowcount)+"rows updated"
		messagebox.showinfo("Success",msg)
		
	except cx_Oracle.DatabaseError as e:
		con.rollback()
		messagebox.showerror("Failure",e)
	finally:
		if cursor is not None:
			cursor.close()
		if con is not None:
			con.close()	
		

upSt=Toplevel(root)
upSt.title("Update Record")
upSt.geometry("400x400+200+200")
upSt.configure(background='ghost white')
upSt.withdraw()


lblUpRno=Label(upSt,text="ENTER ROLL NO")
lblUpName=Label(upSt,text="ENTER UPDATED NAME")
lblUpMarks=Label(upSt,text="ENTER UPDATED MARKS")
entUpRno=Entry(upSt ,bd=5)
entUpName=Entry(upSt ,bd=5)
entUpMarks=Entry(upSt ,bd=5)
btnUpUpdate=Button(upSt,background='linen',text="UPDATE",font=('arial',12,'bold'),width=10 , command=f8 )
btnUpBack=Button(upSt,background='linen',text="BACK",font=('arial',12,'bold'),width=10, command=f7)

lblUpRno.pack(pady=10)
entUpRno.pack(pady=10)
lblUpName.pack(pady=10)
entUpName.pack(pady=10)
lblUpMarks.pack(pady=10)
entUpMarks.pack(pady=10)
btnUpUpdate.pack(pady=10)
btnUpBack.pack(pady=10)

def f11():
	root.deiconify()
	delSt.withdraw()

def f10():
	con=None
	cursor=None
	try:
		con=cx_Oracle.connect("system/abc123")
		
		srno=entDelRno.get()
		if srno.isdigit() and int(srno)>0:
			rno=int(srno)
		else:
			messagebox.showerror("mistake","incorrect rno")
			entAddRno.focus()
			return
		cursor=con.cursor()
		sql="delete from student where rno='%d'"
		args=(rno)	
		cursor.execute(sql % args)
		con.commit()
		msg=str(cursor.rowcount)+"rows Deleted"
		messagebox.showinfo("Success",msg)
			
	except cx_Oracle.DatabaseError as e:
		con.rollback()
		messagebox.showerror("Failure",e)
	finally:
		if cursor is not None:
			cursor.close()
		if con is not None:
			con.close()	
		entDelRno.delete(0,END)

delSt=Toplevel(root)
delSt.title("Delete Record")
delSt.geometry("400x400+200+200")
delSt.configure(background='ghost white')
delSt.withdraw()


lblDelRno=Label(delSt,text="ENTER ROLL NO")
entDelRno=Entry(delSt,bd=5)
btnDelDelete=Button(delSt,text="DELETE",background='linen',font=('arial',12,'bold'),width=10,command=f10)
btnDelBack=Button(delSt,text="BACK",background='linen',font=('arial',12,'bold'),width=10,command=f11)

lblDelRno.pack(pady=10)
entDelRno.pack(pady=10)
btnDelDelete.pack(pady=10)
btnDelBack.pack(pady=10)







root.mainloop()
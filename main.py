from tkinter import *
from tkinter import messagebox
from datetime import datetime
import mysql.connector
from mysql.connector import Error

def connect_db():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="pizza_system"
        )
        return conn
    except Error as e:
        messagebox.showerror("Database Error", "Cannot connect to database!")
        return None

def save_order():
    name = txtname.get().strip()
    phone = txtphone.get().strip()
    qty1 = int(spin1.get())
    qty2 = int(spin2.get())

    if name == "":
        messagebox.showwarning("Warning", "Please enter customer name!")
        return
    if phone == "":
        messagebox.showwarning("Warning", "Please enter phone number!")
        return
    if var1.get() == 0 and var2.get() == 0:
        messagebox.showwarning("Warning", "Please select at least one pizza!")
        return

    total = 0
    if var1.get() == 1:
        total += qty1 * 25
    if var2.get() == 1:
        total += qty2 * 20

    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            sql = "INSERT INTO pizza_orders (customer_name, phone_number, beef_qty, chicken_qty, total_amount) VALUES (%s, %s, %s, %s, %s)"
            values = (name, phone, qty1, qty2, total)
            cursor.execute(sql, values)
            conn.commit()
            messagebox.showinfo("Success", "Order saved to database!")
        except Error as e:
            messagebox.showerror("Error", "Failed to save order!")
        finally:
            conn.close()

def check_records():
    conn = connect_db()
    if not conn:
        return

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM pizza_orders")
        results = cursor.fetchall()

        record_win = Toplevel(top)
        record_win.title("All Orders Record")
        record_win.geometry("500x450")
        record_win.config(bg="lightblue")

        Label(record_win, text="PIZZA ORDER RECORDS", bg="lightblue", font=("Arial", 16, "italic")).pack(pady=10)
        Label(record_win, text="----------------------------------------", bg="lightblue").pack()

        Label(record_win, text="ID", bg="lightblue", font=("Arial", 11, "bold")).place(x=20, y=60)
        Label(record_win, text="Name", bg="lightblue", font=("Arial", 11, "bold")).place(x=100, y=60)
        Label(record_win, text="Phone", bg="lightblue", font=("Arial", 11, "bold")).place(x=220, y=60)
        Label(record_win, text="Beef", bg="lightblue", font=("Arial", 11, "bold")).place(x=340, y=60)
        Label(record_win, text="Chicken", bg="lightblue", font=("Arial", 11, "bold")).place(x=400, y=60)
        Label(record_win, text="Total", bg="lightblue", font=("Arial", 11, "bold")).place(x=460, y=60)

        Label(record_win, text="----------------------------------------", bg="lightblue").place(x=20, y=85)

        line = 100

        for row in results:
            Label(record_win, text=str(row[0]), bg="lightblue", font=("Arial", 10)).place(x=20, y=line)
            Label(record_win, text=str(row[1]), bg="lightblue", font=("Arial", 10)).place(x=100, y=line)
            Label(record_win, text=str(row[2]), bg="lightblue", font=("Arial", 10)).place(x=220, y=line)
            Label(record_win, text=str(row[3]), bg="lightblue", font=("Arial", 10)).place(x=340, y=line)
            Label(record_win, text=str(row[4]), bg="lightblue", font=("Arial", 10)).place(x=400, y=line)
            Label(record_win, text=f"RM {row[5]:.2f}", bg="lightblue", font=("Arial", 10)).place(x=460, y=line)
            line = line + 25

    except Error as e:
        messagebox.showerror("Error", "Cannot load records!")
    finally:
        conn.close()

top = Tk()
top.title("Pizza Order System")
top.geometry("600x450")
top.eval("tk::PlaceWindow . center")
top.config(bg="coral")

txtname = StringVar()
txtphone = StringVar()
var1 = IntVar()
var2 = IntVar()

label = Label(top, text="PIZZA ORDER SYSTEM", bg="coral", font=("Arial", 18))
label.pack(pady=10)

name = Label(top, text="Customer : ", bg="coral", font=("Arial", 13))
name.place(x=20, y=60)

e1 = Entry(top, width=17, textvariable=txtname, font=("Arial", 13))
e1.place(x=110, y=60)

phone = Label(top, text="Phone Number : ", bg="coral", font=("Arial", 13))
phone.place(x=300, y=60)

e2 = Entry(top, width=15, textvariable=txtphone, font=("Arial", 13))
e2.place(x=430, y=60)

fill = Label(top, text="*Please fill the order form", bg="coral", font=("Arial", 13))
fill.place(x=30, y=100)

types = Label(top, text="Types of Pizza", bg="coral", font=("Arial", 13, "bold"))
types.place(x=70, y=140)

quantity = Label(top, text="Quantity", bg="coral", font=("Arial", 13, "bold"))
quantity.place(x=300, y=140)

price = Label(top, text="Price (RM)", bg="coral", font=("Arial", 13, "bold"))
price.place(x=470, y=140)

chk1 = Checkbutton(top, text="Beef Pepperoni RM 25/Set", variable=var1, bg="coral", font=("Arial", 12))
chk1.place(x=20, y=170)

chk2 = Checkbutton(top, text="Chicken Pepperoni RM 20/Set", variable=var2, bg="coral", font=("Arial", 12))
chk2.place(x=20, y=200)

spin1 = Spinbox(top, from_=0, to=30, width=5)
spin1.place(x=290, y=170)

spin2 = Spinbox(top, from_=0, to=30, width=5)
spin2.place(x=290, y=200)

price1 = Label(top, text="0", bg="coral", font=("Arial", 12))
price1.place(x=480, y=170)

price2 = Label(top, text="0", bg="coral", font=("Arial", 12))
price2.place(x=480, y=200)

def update_price():
    quantity1 = int(spin1.get())
    quantity2 = int(spin2.get())

    total1 = 25 * quantity1 if var1.get() else 0
    total2 = 20 * quantity2 if var2.get() else 0

    price1.config(text=str(total1))
    price2.config(text=str(total2))

spin1.config(command=update_price)
spin2.config(command=update_price)

def calculate_order():
    total = 0
    order_details = ""

    quantity1 = int(spin1.get())
    quantity2 = int(spin2.get())

    if var1.get() == 1:
        total += quantity1 * 25
        order_details += f"BEEF PEPPERONI  (Quantity: {quantity1})\n"

    if var2.get() == 1:
        total += quantity2 * 20
        order_details += f"CHICKEN PEPPERONI  (Quantity: {quantity2})\n"

    output = f"""
CUSTOMER ORDER
NAME: {txtname.get()} 
PHONE NUMBER: {txtphone.get()}

ORDER
{order_details}
TOTAL PRICE RM {total:.2f}
    """
    messagebox.showinfo("Order Summary", output)
    save_order()

def show_receipt():
    qty1 = int(spin1.get())
    qty2 = int(spin2.get())

    total = 0
    if var1.get() == 1:
        total += qty1 * 25
    if var2.get() == 1:
        total += qty2 * 20

    receipt_win = Toplevel(top)
    receipt_win.title("Pizza Receipt")
    receipt_win.geometry("400x400")
    receipt_win.config(bg="pink")

    Label(receipt_win, text="Pizza Order Receipt", bg="pink", font=("Arial", 16, "italic")).pack(pady=10)

    Label(receipt_win, text="CUSTOMER", fg="red", bg="pink", font=("Arial", 12, "bold", "underline")).pack()
    Label(receipt_win, text=f"NAME: {txtname.get().upper()}", bg="pink", font=("Arial", 11)).pack()
    Label(receipt_win, text=f"PHONE NUMBER: {txtphone.get()}", bg="pink", font=("Arial", 11)).pack(pady=(0, 10))

    frame = Frame(receipt_win, bg="pink")
    frame.pack()

    Label(frame, text="TYPES OF PIZZA", fg="blue", bg="pink", font=("Arial", 11, "bold", "underline"), width=15).grid(row=0, column=0)
    Label(frame, text="QUANTITY", fg="red", bg="pink", font=("Arial", 11, "bold", "underline"), width=10).grid(row=0, column=1)
    Label(frame, text="PRICE (RM)", fg="blue", bg="pink", font=("Arial", 11, "bold", "underline"), width=10).grid(row=0, column=2)

    row_num = 1
    if var1.get() == 1:
        Label(frame, text="BEEF PEPPERONI", bg="pink", font=("Arial", 10)).grid(row=row_num, column=0)
        Label(frame, text=str(qty1), bg="pink", font=("Arial", 10)).grid(row=row_num, column=1)
        Label(frame, text=str(qty1 * 25), bg="pink", font=("Arial", 10)).grid(row=row_num, column=2)
        row_num += 1

    if var2.get() == 1:
        Label(frame, text="CHICKEN PEPPERONI", bg="pink", font=("Arial", 10)).grid(row=row_num, column=0)
        Label(frame, text=str(qty2), bg="pink", font=("Arial", 10)).grid(row=row_num, column=1)
        Label(frame, text=str(qty2 * 20), bg="pink", font=("Arial", 10)).grid(row=row_num, column=2)

    Label(receipt_win, text=f"TOTAL PAYMENT     RM {total:.2f}", fg="red", bg="pink", font=("Arial", 14, "bold")).pack(pady=20)

btn_pay = Button(top, text="PAYMENT", bg="green", fg="white", font=("Arial", 12, "bold"), command=calculate_order)
btn_pay.place(x=400, y=250)

btn_receipt = Button(top, text="PRINT RECEIPT", bg="orange", font=("Arial", 12, "bold"), command=show_receipt)
btn_receipt.place(x=400, y=300)

btn_check = Button(top, text="CHECK RECORDS", bg="blue", fg="white", font=("Arial", 12, "bold"), command=check_records)
btn_check.place(x=400, y=350)

top.mainloop()
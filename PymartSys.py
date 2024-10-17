#Project Pymart
import random
import tkinter as tk
from tkinter import ttk
from VerifySystem.VerifyIdentity import *
from DataFolder.DataClass import *

EntryStatus = True
Select_itemsIntocart = True
CartValidator = {}
CartSave = {}
DisplayTotal = 0
CurrentLocation = ""

#def Receipt
import tkinter as tk
from tkinter import ttk

# Def of Receipt
def show_receipt(CartValidator, DeliveryFee, DisplayTotal):
    root = tk.Tk()
    root.title("Pymart Receipt")
    root.attributes('-topmost', True)
    style = ttk.Style()
    style.configure("Treeview", font=("Helvetica", 12))
    style.configure("Treeview.Heading", font=("Helvetica", 14, "bold"))

    tree = ttk.Treeview(root, columns=("สินค้า", "จำนวน", "ราคา"), show='headings')
    tree.heading("สินค้า", text="สินค้า")
    tree.column("สินค้า", width=200)
    tree.heading("จำนวน", text="จำนวน")
    tree.column("จำนวน", width=100)
    tree.heading("ราคา", text="ราคา")
    tree.column("ราคา", width=100)

    for item, details in CartValidator.items():
        total_price = details['ราคา']
        quantity = details['จำนวน']
        price_per_item = total_price / quantity 
        tree.insert("", "end", values=(item, quantity, total_price))

    scrollbar = ttk.Scrollbar(root, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side='right', fill='y')
    tree.pack(expand=True, fill='both')

    info_frame = tk.Frame(root)
    info_frame.pack(side='right', padx=10, pady=10)

    delivery_fee_label = tk.Label(info_frame, text=f"ค่าส่ง: {DeliveryFee} บาท", font=("Helvetica", 12))
    delivery_fee_label.pack(pady=(0, 10))

    total_label = tk.Label(info_frame, text=f"รวมสุทธิ: {DisplayTotal} บาท", font=("Helvetica", 12))
    total_label.pack()

    root.mainloop()

#def of CartOptimize
def show_cart():
    if not CartValidator:
        print("ไม่มีสินค้าในรถเข็น\n")
        return
    global DisplayTotal
    DisplayTotal = 0
    print("\nสินค้าในรถเข็น:")
    for index, (item_name, item_details) in enumerate(CartValidator.items(), start=1):
        item_total_price = item_details['จำนวน'] * CartSave[item_name]['ราคา']
        print(f"{index}. {item_name} จำนวน: {item_details['จำนวน']} ชิ้น ราคา: {item_details['ราคา']} บาท (รวม: {item_total_price} บาท)")
        DisplayTotal += item_total_price

def Check_Command(command):
    global DisplayTotal
    try:
        if 'm' in command:
            number_str, amount_str = command.split('m')
            item_index = int(number_str) - 1 
            amount = int(amount_str)
            item_name = list(CartValidator.keys())[item_index]
            if item_name in CartValidator:
                if CartValidator[item_name]['จำนวน'] > amount:
                    CartValidator[item_name]['จำนวน'] -= amount
                    CartValidator[item_name]['ราคา'] -= CartSave[item_name]['ราคา'] * amount
                    DisplayTotal -= CartSave[item_name]['ราคา'] * amount
                    print(f"ลดจำนวน {amount} ของ {item_name} เหลือ {CartValidator[item_name]['จำนวน']} ชิ้น")
                else:
                    DisplayTotal -= CartSave[item_name]['ราคา'] * CartValidator[item_name]['จำนวน']
                    del CartValidator[item_name]
                    print(f"{item_name} ถูกลบออกจากรถเข็น")

        elif 'p' in command:
            number_str, amount_str = command.split('p')
            item_index = int(number_str) - 1
            amount = int(amount_str)
            item_name = list(CartValidator.keys())[item_index]
            if item_name in CartValidator:
                CartValidator[item_name]['จำนวน'] += amount
                CartValidator[item_name]['ราคา'] += CartSave[item_name]['ราคา'] * amount
                DisplayTotal += CartSave[item_name]['ราคา'] * amount
                print(f"เพิ่มจำนวน {amount} ของ {item_name} ตอนนี้มี {CartValidator[item_name]['จำนวน']} ชิ้น")

        elif command.lower() == "back":
            print("")
            return False

        else:
            print("คำสั่งไม่ถูกต้อง กรุณาป้อนคำสั่งอีกครั้ง")

    except (ValueError, IndexError):
        print("เกิดข้อผิดพลาด: กรุณาตรวจสอบคำสั่งที่ป้อน")

def CheckCart():
    print("\n\nกรุณาป้อนคำสั่ง")
    print("(เบอร์)m(จำนวน) -> เป็นการลบสินค้า")
    print("(เบอร์)p(จำนวน) -> เป็นการเพิ่มสินค้า")
    print("back -> กลับ")
    while True:
        show_cart()
        command = input(">>>> ")
        if Check_Command(command) is False:
            break

#def of Num
def Numorder():
    indexOrder = 1
    for Class_name in ProductList.keys():
        print(f"{indexOrder}. {Class_name}")
        indexOrder += 1
    print(f"\nราคาสุทธิ {DisplayTotal} บาท")
    print(CartValidator)

def NumGoods(Goods_of_result):
    indexGoods = 1
    for goods_name, goods_values in Goods_of_result.items():
        print(f"{indexGoods}. {goods_name} ราคา {goods_values} บาท")
        indexGoods += 1

#Select from dict
def selectClass(number):
    Classname = list(ProductList.keys())[number - 1]
    func = ProductList.get(Classname)
    if func:
        return func()

def select_items(addItemsIntoCart, Goods_of_result):
    global DisplayTotal
    for item_number in addItemsIntoCart:
        try:
            item_index = int(item_number) - 1
            items_name = list(Goods_of_result.keys())[item_index]
            item_price = Goods_of_result[items_name]
            if items_name in CartValidator:
                CartValidator[items_name]['จำนวน'] += 1
                CartValidator[items_name]['ราคา'] += item_price
            else:
                CartValidator[items_name] = {'จำนวน': 1, 'ราคา': item_price}
            if items_name not in CartSave:
                CartSave[items_name] = {}
            CartSave[items_name]['ราคา'] = item_price
            DisplayTotal += item_price
            print(f"เพิ่ม {items_name} ลงในรถเข็น จำนวน 1 ชิ้น ราคา {item_price} บาท")
        except (IndexError, ValueError):
            print("!!!หมายเลขสินค้าหมายเลขไม่ถูกต้อง")

#Check Status
if SelectVerify == 1:
    EntryStatus = True
    while EntryStatus == True:
        Checkbought_Status = str(input("คุณต้องการที่จะซื้อของหรือไม่(Y/N): "))
        if (Checkbought_Status.isdigit()):
            print("กรุณากรอกเป็นข้อความ.")
        elif (Checkbought_Status.upper() not in ["Y", "YES", "N", "NO"]):
            print("กรุณากรอกให้ถูกต้อง")
        if (Checkbought_Status.upper() == "Y") or (Checkbought_Status.upper()) == "YES":
            SelectStatus = True
            while SelectStatus == True:
                print("คุณจะเลือกหมวดหมู่ใด")
                Numorder()
                try:
                    user_choice = input("-------------------------------------------\nเลือกเลขของหมวดหมู่ที่ต้องการ[พิมพ์ 0 เพื่อกลับ ,พิมพ์ cv เช็คตะกร้า]: ").strip()
                    if user_choice.lower() == "cv":
                        CheckCart()
                        continue
                    elif user_choice == "0":
                        SelectStatus = False
                        Checkbought_Status = "N"
                    elif user_choice.isdigit():
                        user_choice = int(user_choice)
                        if 1 <= user_choice <= len(ProductList):
                            result = selectClass(user_choice)
                            print("รายการสินค้าในหมวดหมู่")
                            NumGoods(result)
                            print("-------------------")
                            Select_itemsIntocart = True
                            while Select_itemsIntocart == True:
                                GoodsItems = input("\nเลือกเลขสินค้าที่ต้องการ (เลือกได้หลายต่อ เช่น 1 4 5 [กด back เพื่อกลับ]): ").strip()
                                if GoodsItems.lower() == "back":
                                    Select_itemsIntocart = False
                                    break
                                GoodsItems = GoodsItems.split()
                                if all(item.isdigit() for item in GoodsItems):
                                    select_items(GoodsItems, result)
                                else:
                                    print("กรุณาใส่หมายเลขสินค้าเท่านั้น\n")
                                    continue
                        else:
                            print("\nหมายเลขหมวดหมู่ไม่ถูกต้อง\n----------------------o")
                    else:
                        print("\nกรุณาใส่หมายเลขหมวดหมู่ที่ถูกต้องหรือคำสั่งที่ถูกต้อง\n")
                except ValueError:
                    print("กรุณาป้อนให้ถูกต้อง")
        if (Checkbought_Status.upper() == "N") or (Checkbought_Status.upper()) == "NO":
            if DisplayTotal == 0:
                print("\no----------------------o \n   ออกจากระบบ   \no----------------------o")
                EntryStatus = False
            elif DisplayTotal > 0:
                print("---------------------------")
                LocateCheck = True
                while LocateCheck == True:
                    CurrentLocation = str(input("กรอกอำเภอปัจจุบัน: ")) #อำเภอสำหรับบวกค่าส่ง
                    if CurrentLocation in ["ศรีราชา"]:
                        DeliveryFee = 20.0
                        LocateCheck = False
                    elif CurrentLocation in ["เมืองชลบุรี", "บางละมุง", "เกาะสีชัง"]:
                        DeliveryFee = 40.0
                        LocateCheck = False
                    elif CurrentLocation in ["บ้านบึง", "พานทอง", "พนัสนิคม", "สัตหีบ", "หนองใหญ่",
                            "บ่อทอง", "เกาะจันทร์", "บางปะกง"]:
                        DeliveryFee = 70.0
                        LocateCheck = False
                    else:
                        print("กรุณาพิมพ์ให้ถูกต้องหรืออยู่ภายในจังหวัดชลบุรี")
                DisplayTotal = DisplayTotal + DeliveryFee
                #How to pay
                ScanQR = True
                try:
                    SelectPayout = int(input("Mobile Banking / ปลายทาง [1/2]: "))
                    if SelectPayout == 1:
                        print(f"ค่าส่ง {DeliveryFee} บาท\nยอดสุทธิ {DisplayTotal} บาท...ScanQR")
                        while ScanQR == True:
                            try:
                                QRloop = int(input("จ่าย: "))
                                if QRloop == DisplayTotal:
                                    RandomDay = random.randint(1,4)
                                    print(f"\n=========================\nขอบคุณ คุณ {AccLogin} ที่ใช้บริการ")
                                    print(f"รอรับของภายใน {RandomDay} วัน")
                                    print(f"ค่าส่ง {DeliveryFee} บาท\nยอดสุทธิ {DisplayTotal} บาท")
                                    show_receipt(CartValidator, DeliveryFee, DisplayTotal)
                                    ScanQR = False
                                elif QRloop != DisplayTotal:
                                    print("กรุณากรอกให้ถูกต้อง")
                                    continue
                            except (ValueError):
                                print("Value Error... ScanQr Again.")
                    elif SelectPayout == 2:
                        print(f"\n=========================\nขอบคุณ คุณ {AccLogin} ที่ใช้บริการ")
                        print(f"ค่าส่ง {DeliveryFee} บาท\nรอเก็บเงินปลายทางยอดสุทธิ {DisplayTotal} บาท")
                        show_receipt(CartValidator, DeliveryFee, DisplayTotal)
                except ValueError:
                    print("กรุณากรอกเลขให้ถูกต้อง")
                EntryStatus = False
elif SelectVerify == 4:
    print()
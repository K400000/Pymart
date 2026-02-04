"""
Receipt Module - สร้างและแสดงใบเสร็จรับเงิน
"""
import tkinter as tk
from tkinter import ttk


def show_receipt(CartValidator, DeliveryFee, DisplayTotal):
    """แสดงใบเสร็จในหน้าต่าง Tkinter"""
    root = tk.Tk()
    root.title("Pymart Receipt")
    root.attributes('-topmost', True)
    
    # ตั้งค่า style
    style = ttk.Style()
    style.configure("Treeview", font=("Helvetica", 12))
    style.configure("Treeview.Heading", font=("Helvetica", 14, "bold"))
    
    # สร้างตารางแสดงสินค้า
    tree = ttk.Treeview(root, columns=("สินค้า", "จำนวน", "ราคา"), show='headings')
    tree.heading("สินค้า", text="สินค้า")
    tree.column("สินค้า", width=200)
    tree.heading("จำนวน", text="จำนวน")
    tree.column("จำนวน", width=100)
    tree.heading("ราคา", text="ราคา")
    tree.column("ราคา", width=100)
    
    # เพิ่มรายการสินค้าในตาราง
    for item, details in CartValidator.items():
        total_price = details['ราคา']
        quantity = details['จำนวน']
        tree.insert("", "end", values=(item, quantity, total_price))
    
    # เพิ่ม scrollbar
    scrollbar = ttk.Scrollbar(root, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side='right', fill='y')
    tree.pack(expand=True, fill='both')
    
    # แสดงข้อมูลค่าส่งและยอดรวม
    info_frame = tk.Frame(root)
    info_frame.pack(side='right', padx=10, pady=10)
    
    delivery_fee_label = tk.Label(
        info_frame, 
        text=f"ค่าส่ง: {DeliveryFee} บาท", 
        font=("Helvetica", 12)
    )
    delivery_fee_label.pack(pady=(0, 10))
    
    total_label = tk.Label(
        info_frame, 
        text=f"รวมสุทธิ: {DisplayTotal} บาท", 
        font=("Helvetica", 12)
    )
    total_label.pack()
    
    root.mainloop()


def print_receipt_console(CartValidator, DeliveryFee, DisplayTotal, username):
    """แสดงใบเสร็จในคอนโซล"""
    print("\n" + "="*50)
    print(" " * 15 + "PYMART RECEIPT")
    print("="*50)
    print(f"ลูกค้า: {username}")
    print("-"*50)
    print(f"{'สินค้า':<20} {'จำนวน':>10} {'ราคา':>15}")
    print("-"*50)
    
    for item, details in CartValidator.items():
        quantity = details['จำนวน']
        price = details['ราคา']
        print(f"{item:<20} {quantity:>10} {price:>15} บาท")
    
    print("-"*50)
    print(f"{'ค่าส่ง:':<20} {' ':>10} {DeliveryFee:>15} บาท")
    print("="*50)
    print(f"{'ยอดรวมสุทธิ:':<20} {' ':>10} {DisplayTotal:>15} บาท")
    print("="*50)
    print("\nขอบคุณที่ใช้บริการ Pymart!")
    print("="*50 + "\n")

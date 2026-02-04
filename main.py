"""
Pymart - Python MiniProject
ระบบร้านค้าออนไลน์
"""
import random
import sys
import os

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    os.system('chcp 65001 >nul 2>&1')  # Set console to UTF-8

# เพิ่ม src folder ใน path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import modules
from src.auth import run_auth_system
from src.cart import (
    show_cart, add_to_cart, manage_cart, 
    get_cart_total, CartValidator, DisplayTotal
)
from src.receipt import show_receipt, print_receipt_console
from src.utils import (
    load_products, display_categories, display_products,
    select_category, get_delivery_location
)


def main():
    """ฟังก์ชันหลักของโปรแกรม"""
    
    # โหลดข้อมูลสินค้า
    ProductList = load_products()
    
    if not ProductList:
        print("ไม่สามารถโหลดข้อมูลสินค้าได้")
        return
    
    # ระบบ Authentication
    SelectVerify, AccLogin = run_auth_system()
    
    # ถ้าผู้ใช้เลือกออกจากระบบ
    if SelectVerify == 4:
        return
    
    # ถ้าผู้ใช้ Login สำเร็จ
    if SelectVerify == 1 and AccLogin:
        print(f"\nยินดีต้อนรับ คุณ {AccLogin}!")
        shopping_loop(AccLogin, ProductList)


def shopping_loop(AccLogin, ProductList):
    """วนลูปการซื้อสินค้า"""
    
    while True:
        Checkbought_Status = str(input("คุณต้องการที่จะซื้อของหรือไม่(Y/N): "))
        
        if Checkbought_Status.isdigit():
            print("กรุณากรอกเป็นข้อความ.")
            continue
        
        if Checkbought_Status.upper() not in ["Y", "YES", "N", "NO"]:
            print("กรุณากรอกให้ถูกต้อง")
            continue
        
        # ถ้าต้องการซื้อ
        if Checkbought_Status.upper() in ["Y", "YES"]:
            category_selection_loop(ProductList)
        
        # ถ้าไม่ต้องการซื้อ
        if Checkbought_Status.upper() in ["N", "NO"]:
            handle_checkout(AccLogin)
            break


def category_selection_loop(ProductList):
    """วนลูปการเลือกหมวดหมู่และสินค้า"""
    
    while True:
        print("\nคุณจะเลือกหมวดหมู่ใด")
        display_categories(ProductList)
        
        # แสดงยอดรวม
        total = get_cart_total()
        print(f"\nราคาสุทธิ {total} บาท")
        
        try:
            user_choice = input(
                "-------------------------------------------\n"
                "เลือกเลขของหมวดหมู่ที่ต้องการ[พิมพ์ 0 เพื่อกลับ ,พิมพ์ cv เช็คตะกร้า]: "
            ).strip()
            
            # เช็คตะกร้า
            if user_choice.lower() == "cv":
                manage_cart()
                continue
            
            # กลับ
            elif user_choice == "0":
                break
            
            # เลือกหมวดหมู่
            elif user_choice.isdigit():
                user_choice = int(user_choice)
                
                if 1 <= user_choice <= len(ProductList):
                    result = select_category(user_choice, ProductList)
                    
                    if result:
                        print("\nรายการสินค้าในหมวดหมู่")
                        display_products(result)
                        print("-------------------")
                        
                        # วนลูปเลือกสินค้า
                        select_products_loop(result)
                else:
                    print("\nหมายเลขหมวดหมู่ไม่ถูกต้อง\n----------------------o")
            else:
                print("\nกรุณาใส่หมายเลขหมวดหมู่ที่ถูกต้องหรือคำสั่งที่ถูกต้อง\n")
                
        except ValueError:
            print("กรุณาป้อนให้ถูกต้อง")


def select_products_loop(products_dict):
    """วนลูปการเลือกสินค้าในหมวดหมู่"""
    
    while True:
        GoodsItems = input(
            "\nเลือกเลขสินค้าที่ต้องการ (เลือกได้หลายตัว เช่น 1 4 5 [กด back เพื่อกลับ]): "
        ).strip()
        
        if GoodsItems.lower() == "back":
            break
        
        GoodsItems = GoodsItems.split()
        
        if all(item.isdigit() for item in GoodsItems):
            add_to_cart(GoodsItems, products_dict)
        else:
            print("กรุณาใส่หมายเลขสินค้าเท่านั้น\n")


def handle_checkout(AccLogin):
    """จัดการการชำระเงิน"""
    
    total = get_cart_total()
    
    # ถ้าไม่มีสินค้าในตะกร้า
    if total == 0:
        print("\no----------------------o \n   ออกจากระบบ   \no----------------------o")
        return
    
    # ถ้ามีสินค้าในตะกร้า
    print("---------------------------")
    
    # รับข้อมูลพื้นที่จัดส่ง
    CurrentLocation, DeliveryFee = get_delivery_location()
    
    # คำนวณยอดรวมพร้อมค่าส่ง
    FinalTotal = total + DeliveryFee
    
    # เลือกวิธีชำระเงิน
    handle_payment(AccLogin, DeliveryFee, FinalTotal, CurrentLocation)


def handle_payment(AccLogin, DeliveryFee, FinalTotal, CurrentLocation):
    """จัดการการชำระเงิน"""
    
    try:
        SelectPayout = int(input("Mobile Banking / ปลายทาง [1/2]: "))
        
        # Mobile Banking
        if SelectPayout == 1:
            print(f"ค่าส่ง {DeliveryFee} บาท\nยอดสุทธิ {FinalTotal} บาท...ScanQR")
            
            while True:
                try:
                    QRloop = int(input("จ่าย: "))
                    
                    if QRloop == FinalTotal:
                        RandomDay = random.randint(1, 4)
                        print(f"\n=========================")
                        print(f"ขอบคุณ คุณ {AccLogin} ที่ใช้บริการ")
                        print(f"รอรับของภายใน {RandomDay} วัน")
                        print(f"ค่าส่ง {DeliveryFee} บาท\nยอดสุทธิ {FinalTotal} บาท")
                        
                        # แสดงใบเสร็จ
                        show_receipt(CartValidator, DeliveryFee, FinalTotal)
                        print_receipt_console(CartValidator, DeliveryFee, FinalTotal, AccLogin)
                        break
                    else:
                        print("กรุณากรอกให้ถูกต้อง")
                        
                except ValueError:
                    print("Value Error... ScanQr Again.")
        
        # ปลายทาง
        elif SelectPayout == 2:
            RandomDay = random.randint(1, 4)
            print(f"\n=========================")
            print(f"ขอบคุณ คุณ {AccLogin} ที่ใช้บริการ")
            print(f"รอรับของภายใน {RandomDay} วัน")
            print(f"ค่าส่ง {DeliveryFee} บาท\nรอเก็บเงินปลายทางยอดสุทธิ {FinalTotal} บาท")
            
            # แสดงใบเสร็จ
            show_receipt(CartValidator, DeliveryFee, FinalTotal)
            print_receipt_console(CartValidator, DeliveryFee, FinalTotal, AccLogin)
        
        else:
            print("กรุณาเลือก 1 หรือ 2")
            
    except ValueError:
        print("กรุณากรอกเลขให้ถูกต้อง")


if __name__ == "__main__":
    main()
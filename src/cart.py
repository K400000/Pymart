"""
Cart Module - จัดการตะกร้าสินค้า
"""

# Global cart variables
CartValidator = {}  # เก็บสินค้าและจำนวนที่ผู้ใช้เลือก
CartSave = {}       # เก็บข้อมูลราคาต่อชิ้นของสินค้า
DisplayTotal = 0    # ราคารวมทั้งหมด


def show_cart():
    """แสดงรายการสินค้าในรถเข็น"""
    global DisplayTotal
    
    if not CartValidator:
        print("ไม่มีสินค้าในรถเข็น\n")
        return
    
    DisplayTotal = 0
    print("\nสินค้าในรถเข็น:")
    for index, (item_name, item_details) in enumerate(CartValidator.items(), start=1):
        item_total_price = item_details['จำนวน'] * CartSave[item_name]['ราคา']
        print(f"{index}. {item_name} จำนวน: {item_details['จำนวน']} ชิ้น "
              f"ราคา: {item_details['ราคา']} บาท (รวม: {item_total_price} บาท)")
        DisplayTotal += item_total_price


def add_to_cart(addItemsIntoCart, Goods_of_result):
    """เพิ่มสินค้าลงในตะกร้า"""
    global DisplayTotal, CartValidator, CartSave
    
    for item_number in addItemsIntoCart:
        try:
            item_index = int(item_number) - 1
            items_name = list(Goods_of_result.keys())[item_index]
            item_price = Goods_of_result[items_name]
            
            # เพิ่มสินค้าในตะกร้า
            if items_name in CartValidator:
                CartValidator[items_name]['จำนวน'] += 1
                CartValidator[items_name]['ราคา'] += item_price
            else:
                CartValidator[items_name] = {'จำนวน': 1, 'ราคา': item_price}
            
            # บันทึกราคาต่อชิ้น
            if items_name not in CartSave:
                CartSave[items_name] = {}
            CartSave[items_name]['ราคา'] = item_price
            
            DisplayTotal += item_price
            print(f"เพิ่ม {items_name} ลงในรถเข็น จำนวน 1 ชิ้น ราคา {item_price} บาท")
            
        except (IndexError, ValueError):
            print("!!!หมายเลขสินค้าหมายเลขไม่ถูกต้อง")


def modify_cart_item(command):
    """แก้ไขจำนวนสินค้าในตะกร้า (เพิ่ม หรือ ลด)"""
    global DisplayTotal, CartValidator, CartSave
    
    try:
        if 'm' in command:  # ลดสินค้า
            number_str, amount_str = command.split('m')
            item_index = int(number_str) - 1
            amount = int(amount_str)
            item_name = list(CartValidator.keys())[item_index]
            
            if item_name in CartValidator:
                if CartValidator[item_name]['จำนวน'] > amount:
                    # ลดจำนวน
                    CartValidator[item_name]['จำนวน'] -= amount
                    CartValidator[item_name]['ราคา'] -= CartSave[item_name]['ราคา'] * amount
                    DisplayTotal -= CartSave[item_name]['ราคา'] * amount
                    print(f"ลดจำนวน {amount} ของ {item_name} เหลือ {CartValidator[item_name]['จำนวน']} ชิ้น")
                else:
                    # ลบออกจากตะกร้า
                    DisplayTotal -= CartSave[item_name]['ราคา'] * CartValidator[item_name]['จำนวน']
                    del CartValidator[item_name]
                    print(f"{item_name} ถูกลบออกจากรถเข็น")
        
        elif 'p' in command:  # เพิ่มสินค้า
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
            return False
        
        else:
            print("คำสั่งไม่ถูกต้อง กรุณาป้อนคำสั่งอีกครั้ง")
    
    except (ValueError, IndexError):
        print("เกิดข้อผิดพลาด: กรุณาตรวจสอบคำสั่งที่ป้อน")
    
    return True


def manage_cart():
    """จัดการตะกร้าสินค้า - แก้ไขจำนวน"""
    print("\n\nกรุณาป้อนคำสั่ง")
    print("(เบอร์)m(จำนวน) -> เป็นการลบสินค้า")
    print("(เบอร์)p(จำนวน) -> เป็นการเพิ่มสินค้า")
    print("back -> กลับ")
    
    while True:
        show_cart()
        command = input(">>>> ")
        if not modify_cart_item(command):
            break


def get_cart_total():
    """คืนค่ายอดรวมในตะกร้า"""
    global DisplayTotal
    return DisplayTotal


def clear_cart():
    """ล้างตะกร้าสินค้า"""
    global CartValidator, CartSave, DisplayTotal
    CartValidator = {}
    CartSave = {}
    DisplayTotal = 0

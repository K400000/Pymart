"""
Utils Module - ฟังก์ชันช่วยเหลือและโหลดข้อมูลสินค้า
"""
import os
import json

# Path to products.json file
PRODUCTS_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "products.json")

# Load products from file
def load_products():
    """โหลดข้อมูลสินค้าจากไฟล์ products.json"""
    try:
        with open(PRODUCTS_FILE, 'r', encoding='utf-8') as f:
            products_data = json.load(f)
        
        # สร้าง ProductList dictionary ที่มี category เป็น key
        # และแต่ละ category มีข้อมูลสินค้าแบบ dictionary
        ProductList = {}
        for category, items in products_data.items():
            # สร้าง closure function สำหรับแต่ละ category
            ProductList[category] = lambda items=items: items
        
        return ProductList
    except FileNotFoundError:
        print(f"Error: ไม่พบไฟล์ {PRODUCTS_FILE}")
        return {}
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return {}
    except Exception as e:
        print(f"Error loading products: {e}")
        return {}


def display_categories(ProductList):
    """แสดงหมวดหมู่สินค้าทั้งหมด"""
    indexOrder = 1
    for Class_name in ProductList.keys():
        print(f"{indexOrder}. {Class_name}")
        indexOrder += 1


def display_products(Goods_of_result):
    """แสดงรายการสินค้าในหมวดหมู่"""
    indexGoods = 1
    for goods_name, goods_values in Goods_of_result.items():
        print(f"{indexGoods}. {goods_name} ราคา {goods_values} บาท")
        indexGoods += 1


def select_category(number, ProductList):
    """เลือกหมวดหมู่สินค้า"""
    try:
        Classname = list(ProductList.keys())[number - 1]
        func = ProductList.get(Classname)
        if func:
            return func()
        return None
    except (IndexError, KeyError):
        return None


def calculate_delivery_fee(location):
    """คำนวณค่าส่งตามพื้นที่"""
    location_fees = {
        "ศรีราชา": 20.0,
        "เมืองชลบุรี": 40.0,
        "บางละมุง": 40.0,
        "เกาะสีชัง": 40.0,
        "บ้านบึง": 70.0,
        "พานทอง": 70.0,
        "พนัสนิคม": 70.0,
        "สัตหีบ": 70.0,
        "หนองใหญ่": 70.0,
        "บ่อทอง": 70.0,
        "เกาะจันทร์": 70.0,
        "บางปะกง": 70.0
    }
    
    return location_fees.get(location, None)


def get_delivery_location():
    """ขอข้อมูลพื้นที่จัดส่งจากผู้ใช้"""
    while True:
        CurrentLocation = str(input("กรอกอำเภอปัจจุบัน: "))
        DeliveryFee = calculate_delivery_fee(CurrentLocation)
        
        if DeliveryFee is not None:
            return CurrentLocation, DeliveryFee
        else:
            print("กรุณาพิมพ์ให้ถูกต้องหรืออยู่ภายในจังหวัดชลบุรี")


def validate_input_is_digit(input_str, error_message="กรุณากรอกเป็นตัวเลข"):
    """ตรวจสอบว่า input เป็นตัวเลขหรือไม่"""
    if input_str.isdigit():
        return True
    else:
        print(error_message)
        return False


def validate_input_is_text(input_str, error_message="กรุณากรอกเป็นข้อความ"):
    """ตรวจสอบว่า input เป็นข้อความหรือไม่"""
    if not input_str.isdigit():
        return True
    else:
        print(error_message)
        return False

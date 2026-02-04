"""
Authentication Module - จัดการระบบ Login และ Register
"""
import json
import random
import os

# Path to users.json file
USERS_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "users.json")

# Load users from JSON file
def load_users():
    """โหลดข้อมูล users จากไฟล์ JSON"""
    try:
        with open(USERS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return {}
    except Exception as e:
        print(f"Error loading users: {e}")
        return {}

# Save users to JSON file
def save_users(account_dict):
    """บันทึกข้อมูล users ลงไฟล์ JSON"""
    try:
        with open(USERS_FILE, 'w', encoding='utf-8') as f:
            json.dump(account_dict, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Error saving users: {e}")

# Global account dictionary
Account = load_users()

# Random OTP Verification for Forget Password
def RandomOTPVerify(ForgetPassVerify):
    """สร้าง OTP และให้ผู้ใช้เปลี่ยนรหัสผ่าน"""
    global Account
    if ForgetPassVerify in Account:
        NumOTP = random.randint(100000, 999999)
        print(f"OTP ของคุณคือ: {NumOTP}")
        
        try:
            CheckInputOF_OTP = int(input("กรุณากรอก OTP >>> "))
            if CheckInputOF_OTP == NumOTP:
                print("<<<-------กรุณากรอกรหัสผ่านใหม่------->>>")
                while True:
                    Newpassword = str(input("NewPassword: "))
                    SamePassword = str(input("กรอกรหัสผ่านซ้ำ: "))
                    if Newpassword == SamePassword:
                        Account[ForgetPassVerify]["password"] = SamePassword
                        save_users(Account)
                        print("รหัสถูกเปลี่ยนเรียบร้อย!!\n----====----====----\n")
                        return True
                    else:
                        print("รหัสผ่านไม่ตรงกัน กรุณากรอกอีกครั้ง")
            else:
                print("OTP ไม่ถูกต้อง")
                return False
        except ValueError:
            print("กรุณากรอกเป็น OTP เท่านั้น")
            return False
    else:
        print("ไม่พบชื่อนี้ในระบบ")
        return False

# Register new user
def Register():
    """สมัครสมาชิกใหม่"""
    global Account
    username = input("กรุณากรอกชื่อผู้ใช้: ")
    
    if username in Account:
        print("ชื่อผู้ใช้นี้มีอยู่แล้ว กรุณาเลือกชื่ือใหม่")
        return None
    
    telephone = input("กรุณากรอกหมายเลขโทรศัพท์: ")
    gmail = input("กรุณากรอกอีเมล: ")
    
    while True:
        password = input("กรุณากรอกรหัสผ่าน: ")
        RegisterPassword = input("กรอกรหัสผ่านซ้ำ: ")
        if password == RegisterPassword:
            break
        else:
            print("รหัสผ่านไม่ตรงกัน กรุณากรอกอีกครั้ง")
    
    # Add to Account dictionary
    Account[username] = {
        "telephone": telephone,
        "gmail": gmail,
        "password": password
    }
    
    # Save to file
    save_users(Account)
    
    print(f"\nข้อมูลของ {username} ถูกเพิ่มเรียบร้อยแล้ว!\n")
    print("\n------------------------->>>\n")
    print(f"Username ของคุณคือ {username}")
    for key in Account[username]:
        print(f"{key} ของคุณคือ {Account[username][key]}")
    print("\n------------------------->>>\n")
    
    return username

# Login function
def Login():
    """เข้าสู่ระบบ"""
    global Account
    while True:
        print("\n-------------------------\n")
        AccLogin = str(input("Username>>> "))
        PassLogin = str(input("Password>>> "))
        
        if AccLogin in Account:
            if PassLogin == Account[AccLogin]["password"]:
                print("เข้าสู่ระบบเรียบร้อย")
                return AccLogin
            else:
                print("รหัสผ่านไม่ถูกต้อง กรุณากรอกใหม่อีกครั้ง")
        else:
            print("ไม่มีรายชื่อนี้อยู่ในระบบ กรอกอีกครั้ง...")

# Main authentication system
def run_auth_system():
    """ระบบ Authentication หลัก - คืนค่า (SelectVerify, AccLogin)"""
    print("<<<<<------ยินดีต้อนรับเข้าสู่ Pymart------>>>>>")
    
    while True:
        try:
            SelectVerify = int(input(
                "กรุณาเลือกเลือกขั้นตอนการเข้าสู่ระบบ(1/2/3/4)\n"
                "1.Login\n"
                "2.Register\n"
                "3.Forget Password\n"
                "4.ออกจากระบบ\n"
                ">>> "
            ))
            
            if SelectVerify == 3:
                ForgetPassVerify = str(input("กรุณากรอก Username: "))
                RandomOTPVerify(ForgetPassVerify)
                
            elif SelectVerify == 2:
                print("กรุณากรอกข้อมูลเพื่อทำการสมัคร")
                Register()
                
            elif SelectVerify == 1:
                AccLogin = Login()
                return SelectVerify, AccLogin
                
            elif SelectVerify == 4:
                print("\no----------------------o \n   ออกจากระบบ   \no----------------------o")
                return SelectVerify, None
                
            else:
                print("กรุณากรอกเป็น (1/2/3/4)\n-----------------\n")
                
        except ValueError:
            print("กรุณากรอกเป็นตัวเลข\n-----------------\n")
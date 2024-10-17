from DataFolder.UserAcc import *
import tkinter as tk
import random
OTPChecking = True
PasswordChecking = True
VerifyIdentity = True
ForgetSystem = True
SystemVerifyOutput = True

#RandomOTP
def RandomOTPVerify(ForgetPassVerify):
    global OTPChecking, PasswordChecking, VerifyIdentity, ForgetSystem
    if ForgetPassVerify in Account:
        while ForgetSystem == True:
            NumOTP = random.randint(100000,999999)
            TimeCount = 20
            if TimeCount != 0:
                while OTPChecking == True:
                    try:
                        CheckInputOF_OTP = int(input(f"{NumOTP}>>> "))
                        if CheckInputOF_OTP == NumOTP:
                            print("<<<-------กรุณากรอกรหัสผ่านใหม่------->>>")
                            while PasswordChecking == True:
                                Newpassword = str(input("NewPassword: "))
                                SamePassword = str(input("กรอกรหัสผ่านซ้ำ: "))
                                if Newpassword == SamePassword:
                                    Account[ForgetPassVerify]["password"] = SamePassword
                                    print("รหัสถูกเปลี่ยนเรียบร้อย!!\n----====----====----\n")
                                    PasswordChecking = False
                                    OTPChecking = False
                                    ForgetSystem = False
                                else:
                                    print("รหัสผ่านไม่ตรงกัน กรุณากรอกอีกครั้ง")
                        else:
                            print("กรุณากรอกใหม่อีกครั้ง")
                    except ValueError:
                        print("กรุณากรอกเป็น OTP เท่านั้น")
            else:
                print("เวลาหมด ดำเนินการรีเซ็ท OTP.!")
    else:
        print("ไม่พบชื่อนี้ในระบบ")

def Register():
    global username, telephone, gmail, password, RegisterPassword
    username = input("กรุณากรอกชื่อผู้ใช้: ")
    telephone = input("กรุณากรอกหมายเลขโทรศัพท์: ")
    gmail = input("กรุณากรอกอีเมล: ")
    while True:
        password = input("กรุณากรอกรหัสผ่าน: ")
        RegisterPassword = (input("กรอกรหัสผ่านซ้ำ: "))
        if password == RegisterPassword:
            break
        else:
            print("รหัสผ่านไม่ตรงกัน กรุณากรอกอีกครั้ง")


#SystemVerifyOutput
print("<<<<<------ยินดีต้อนรับเข้าสู่ Pymart------>>>>>")
while SystemVerifyOutput == True:
    try:
        while VerifyIdentity == True:
            SelectVerify = int(input("กรุณาเลือกเลือกขั้นตอนการเข้าสู่ระบบ(1/2/3/4)\n1.Login\n2.Register\n3.Forget Password\n4.ออกจากระบบ\n>>> "))
            try:
                if SelectVerify == 3:
                    ForgetPassVerify = str(input("กรุณากรอก Username: "))
                    RandomOTPVerify(ForgetPassVerify)
                elif SelectVerify == 2:
                    print("กรุณากรอกข้อมูลเพื่อทำการสมัคร")
                    Register()
                    Account[username] = {
                        "telephone": telephone,
                        "gmail": gmail,
                        "password": password
                    }
                    print(f"\nข้อมูลของ {username} ถูกเพิ่มเรียบร้อยแล้ว!\n")

                    #Show info about Register
                    print("\n------------------------->>>\n")
                    print(f"Username ของคุณคือ {username}")
                    for i in Account[username]:
                        print(f"{i} ของคุณคือ {Account[username][i]}")
                    print("\n------------------------->>>\n")
                elif SelectVerify == 1:
                    while True:
                        print("\n-------------------------\n")
                        AccLogin = str(input("Username>>> "))
                        PassLogin = str(input("Password>>> "))
                        if AccLogin in Account:
                            if PassLogin == Account[AccLogin]["password"]:
                                print("เข้าสู่ระบบเรียบร้อย")
                                VerifyIdentity = False
                                SystemVerifyOutput = False
                                break
                            elif PassLogin != Account[AccLogin]["password"]:
                                print("รหัสผ่านไม่ถูกต้อง กรุณากรอกใหม่อีกครั้ง")
                        elif AccLogin not in Account:
                            print("ไม่มีรายชื่อนี้อยู่ในระบบ กรอกอีกครั้ง...")
                elif SelectVerify == 4:
                    print("\no----------------------o \n   ออกจากระบบ   \no----------------------o")
                    SystemVerifyOutput = False
                    break
                else:
                    print("กรุณากรอกเป็น (1/2/3/4)\n-----------------\n")
            except ValueError:
                print("กรุณากรอกให้ถูกต้อง")
    except ValueError:
        print("กรุณากรอกเป็นตัวเลข\n-----------------\n")
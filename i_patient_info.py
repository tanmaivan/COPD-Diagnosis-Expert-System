from experta import *

class PatientInfo(Fact):
    """
    Fact lưu trữ thông tin cá nhân của bệnh nhân.
    Các thuộc tính:
    - full_name: Họ tên của bệnh nhân.
    - date_of_birth: Ngày sinh của bệnh nhân.
    - gender: Giới tính của bệnh nhân.
    - age: Tuổi của bệnh nhân.
    - address: Địa chỉ của bệnh nhân.
    - phone_number: Số điện thoại của bệnh nhân.
    """
    full_name = Field(str)
    date_of_birth = Field(str)
    gender = Field(str)
    age = Field(int)
    address = Field(str)
    phone_number = Field(str)

class PatientInfoEngine(KnowledgeEngine):
    @Rule(PatientInfo(full_name=MATCH.full_name, date_of_birth=MATCH.date_of_birth, gender=MATCH.gender,
                      age=MATCH.age, address=MATCH.address, phone_number=MATCH.phone_number))
    def display_patient_info(self, full_name, date_of_birth, gender, age, address, phone_number):
        print(f"Patient Information:\n"
              f"Full Name: {full_name}\n"
              f"Date of Birth: {date_of_birth}\n"
              f"Gender: {gender}\n"
              f"Age: {age}\n"
              f"Address: {address}\n"
              f"Phone Number: {phone_number}")

def input_patient_info():
    full_name = input("Enter full name: ")
    date_of_birth = input("Enter date of birth (YYYY-MM-DD): ")
    gender = input("Enter gender: ")
    age = int(input("Enter age: "))
    address = input("Enter address: ")
    phone_number = input("Enter phone number: ")

    return PatientInfo(full_name=full_name, date_of_birth=date_of_birth, gender=gender, age=age, address=address, phone_number=phone_number)

if __name__ == "__main__":
    engine = PatientInfoEngine()
    engine.reset()
    patient_info = input_patient_info()
    engine.declare(patient_info)
    engine.run()
from experta import *

class Patient(Fact):
    """Thông tin bệnh nhân"""
    pass

class BiPAPIndicationExpert(KnowledgeEngine):
    def __init__(self):
        super().__init__()
        self.result = ""

    # Đợt cấp khi có ít nhất 2 tiêu chuẩn
    @Rule(Patient(dyspnea_severe=MATCH.dyspnea_severe, 
                  ph=MATCH.ph, 
                  pco2=MATCH.pco2, 
                  respiratory_rate=MATCH.respiratory_rate,
                  persistent_hypoxemia=MATCH.persistent_hypoxemia),
          TEST(lambda dyspnea_severe, ph, pco2, respiratory_rate, persistent_hypoxemia: 
               sum([
                   dyspnea_severe,
                   ph <= 7.35,
                   pco2 >= 45,
                   respiratory_rate > 25,
                   persistent_hypoxemia
               ]) >= 2))
    def acute_criteria(self):
        self.result = "Bệnh nhân cần được xem xét thông khí nhân tạo không xâm nhập (BiPAP)."
        print(self.result)

    # Trường hợp suy hô hấp mạn: PaCO2 ≥ 50 mmHg
    @Rule(Patient(pco2=MATCH.pco2), TEST(lambda pco2: pco2 >= 50))
    def chronic_resp_failure(self):
        self.result = "Bệnh nhân suy hô hấp mạn cần thông khí nhân tạo không xâm nhập (BiPAP)."
        print(self.result)

def main():
    engine = BiPAPIndicationExpert()
    engine.reset()

    # Nhập thông tin bệnh nhân
    print("Đánh giá các tiêu chuẩn:")
    dyspnea_severe = input("Khó thở vừa tới nặng có co kéo cơ hô hấp phụ và hô hấp nghịch thường (True/False): ").lower() == "true"
    ph = float(input("Nhập pH: "))
    pco2 = float(input("Nhập PaCO2 (mmHg): "))
    respiratory_rate = int(input("Tần số thở (lần/phút): "))
    persistent_hypoxemia = input("Giảm oxy máu dai dẳng dù đã dùng oxy liệu pháp (True/False): ").lower() == "true"

    # Khai báo dữ liệu vào hệ thống
    engine.declare(Patient(
        dyspnea_severe=dyspnea_severe,
        ph=ph,
        pco2=pco2,
        respiratory_rate=respiratory_rate,
        persistent_hypoxemia=persistent_hypoxemia
    ))
    engine.run()

    if not engine.result:
        print("Không có chỉ định thông khí nhân tạo không xâm nhập (BiPAP) cho bệnh nhân.")

if __name__ == "__main__":
    main()

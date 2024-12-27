from experta import *

class BiPAPIndicationFacts(Fact):
    """
    Thông tin bệnh nhân:
    - dyspnea_severe: Khó thở vừa tới nặng có co kéo cơ hô hấp phụ và hô hấp nghịch thường (True/False).
    - ph: Độ pH máu.
    - pco2: Áp lực CO2 động mạch (mmHg).
    - respiratory_rate: Tần số thở (lần/phút).
    - persistent_hypoxemia: Giảm oxy máu dai dẳng dù đã dùng oxy liệu pháp (True/False).
    - bipap_indicated: Chỉ định BiPAP (True/False).
    """
    dyspnea_severe = Field(bool)
    ph = Field(float)
    pco2 = Field(float)
    respiratory_rate = Field(int)
    persistent_hypoxemia = Field(bool)
    bipap_indicated = Field(bool, default=False)

class BiPAPIndicationExpert(KnowledgeEngine):
    @Rule(BiPAPIndicationFacts(dyspnea_severe=MATCH.dyspnea_severe, 
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
        self.declare(BiPAPIndicationFacts(bipap_indicated=True))
        print("Bệnh nhân cần được xem xét thông khí nhân tạo không xâm nhập (BiPAP).")

    @Rule(BiPAPIndicationFacts(pco2=MATCH.pco2), TEST(lambda pco2: pco2 >= 50))
    def chronic_resp_failure(self):
        self.declare(BiPAPIndicationFacts(bipap_indicated=True))
        print("Bệnh nhân suy hô hấp mạn cần thông khí nhân tạo không xâm nhập (BiPAP).")

def main():
    engine = BiPAPIndicationExpert()
    engine.reset()

    print("Đánh giá các tiêu chuẩn:")
    dyspnea_severe = input("Khó thở vừa tới nặng có co kéo cơ hô hấp phụ và hô hấp nghịch thường (True/False): ").lower() == "true"
    ph = float(input("Nhập pH: "))
    pco2 = float(input("Nhập PaCO2 (mmHg): "))
    respiratory_rate = int(input("Tần số thở (lần/phút): "))
    persistent_hypoxemia = input("Giảm oxy máu dai dẳng dù đã dùng oxy liệu pháp (True/False): ").lower() == "true"

    engine.declare(BiPAPIndicationFacts(
        dyspnea_severe=dyspnea_severe,
        ph=ph,
        pco2=pco2,
        respiratory_rate=respiratory_rate,
        persistent_hypoxemia=persistent_hypoxemia
    ))
    engine.run()

if __name__ == "__main__":
    main()
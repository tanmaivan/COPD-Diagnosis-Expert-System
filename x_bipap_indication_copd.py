from experta import *

class BiPAPIndicationFacts(Fact):
    """
    Thông tin bệnh nhân:
    - dyspnea_severe: Khó thở vừa tới nặng có co kéo cơ hô hấp phụ và hô hấp nghịch thường (True/False).
    - ph: Độ pH máu.
    - paco2: Áp lực CO2 động mạch (mmHg).
    - respiratory_rate: Tần số thở (lần/phút).
    - persistent_hypoxemia: Giảm oxy máu dai dẳng dù đã dùng oxy liệu pháp (True/False).
    - bipap_indicated: Chỉ định BiPAP (True/False).
    - bipap_indicated_description: Mô tả chỉ định BiPAP.
    """
    dyspnea_severe = Field(bool)
    ph = Field(int)
    paco2 = Field(float)
    respiratory_rate = Field(int)
    persistent_hypoxemia = Field(bool)
    bipap_indicated = Field(bool, default=False)
    bipap_indicated_description = Field(str, default="")

class BiPAPIndicationExpert(KnowledgeEngine):
    @Rule(BiPAPIndicationFacts(paco2=MATCH.paco2), TEST(lambda paco2: paco2 >= 50))
    def chronic_resp_failure(self):
        bipap_indicated_description = "Bệnh nhân suy hô hấp mạn cần thông khí nhân tạo không xâm nhập (BiPAP)."
        print(bipap_indicated_description)
        self.declare(BiPAPIndicationFacts(bipap_indicated=True, bipap_indicated_description=bipap_indicated_description))
        self.halt()

    @Rule(BiPAPIndicationFacts(dyspnea_severe=MATCH.dyspnea_severe, 
                               ph=MATCH.ph, 
                               paco2=MATCH.paco2, 
                               respiratory_rate=MATCH.respiratory_rate,
                               persistent_hypoxemia=MATCH.persistent_hypoxemia),
          TEST(lambda dyspnea_severe, ph, paco2, respiratory_rate, persistent_hypoxemia: 
               sum([
                   dyspnea_severe,
                   ph <= 7.35,
                   paco2 >= 45,
                   respiratory_rate > 25,
                   persistent_hypoxemia
               ]) >= 2))
    def acute_criteria(self):
        bipap_indicated_description = "Bệnh nhân cần được xem xét thông khí nhân tạo không xâm nhập (BiPAP)."
        print(bipap_indicated_description)
        self.declare(BiPAPIndicationFacts(bipap_indicated=True, bipap_indicated_description=bipap_indicated_description))

def main():
    engine = BiPAPIndicationExpert()
    engine.reset()

    print("Đánh giá các tiêu chuẩn:")
    dyspnea_severe = input("Khó thở vừa tới nặng có co kéo cơ hô hấp phụ và hô hấp nghịch thường (True/False): ").lower() == "true"
    ph = float(input("Nhập pH: "))
    paco2 = float(input("Nhập PaCO2 (mmHg): "))
    respiratory_rate = int(input("Tần số thở (lần/phút): "))
    persistent_hypoxemia = input("Giảm oxy máu dai dẳng dù đã dùng oxy liệu pháp (True/False): ").lower() == "true"

    engine.declare(BiPAPIndicationFacts(
        dyspnea_severe=dyspnea_severe,
        ph=ph,
        paco2=paco2,
        respiratory_rate=respiratory_rate,
        persistent_hypoxemia=persistent_hypoxemia
    ))
    engine.run()

if __name__ == "__main__":
    main()
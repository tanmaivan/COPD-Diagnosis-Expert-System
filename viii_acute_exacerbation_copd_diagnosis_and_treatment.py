from experta import *

class COPDExacerbationFacts(Fact):
    """
    Class COPDExacerbationFacts lưu trữ các thông tin liên quan đến bệnh nhân bị đợt cấp COPD.
    Các thuộc tính bao gồm:
    - vas: Thang điểm đau (Visual Analog Scale)
    - respiratory_rate: Tần số hô hấp
    - heart_rate: Tần số tim
    - spo2: Độ bão hòa oxy trong máu
    - crp: Nồng độ C-reactive protein
    - pao2: Áp suất oxy trong máu động mạch
    - paco2: Áp suất CO2 trong máu động mạch
    - ph: Độ pH của máu
    - diagnosis: Kết quả chẩn đoán
    - treatment_location: Địa điểm điều trị
    """
    vas = Field(int)
    respiratory_rate = Field(int)
    heart_rate = Field(int)
    spo2 = Field(int)
    crp = Field(int)
    pao2 = Field(float)
    paco2 = Field(float)
    ph = Field(float)
    diagnosis = Field(str)
    treatment_location = Field(str)

class COPDExacerbationDiagnosis(KnowledgeEngine):
    
    @Rule(COPDExacerbationFacts(
        vas=P(lambda vas: vas < 5),
        respiratory_rate=P(lambda rr: rr < 24),
        heart_rate=P(lambda hr: hr < 95),
        spo2=P(lambda spo2: spo2 >= 92),
        crp=P(lambda crp: crp < 10)
    ))
    def mild_exacerbation(self):
        self.declare(COPDExacerbationFacts(diagnosis="mild", treatment_location="outpatient"))
        print("Chẩn đoán: Đợt cấp nhẹ. Nên điều trị ngoại trú.")

    @Rule(COPDExacerbationFacts(
        vas=MATCH.vas,
        respiratory_rate=MATCH.respiratory_rate,
        heart_rate=MATCH.heart_rate,
        spo2=MATCH.spo2,
        crp=MATCH.crp),
        TEST(lambda vas, respiratory_rate, heart_rate, spo2, crp: sum([
            vas >= 5,
            respiratory_rate >= 24,
            heart_rate >= 95,
            spo2 < 92,
            crp >= 10
        ]) >= 3)
    )
    def moderate_exacerbation(self):
        self.declare(COPDExacerbationFacts(severity="moderate", treatment_location="internal"))
        print("Chẩn đoán: Đợt cấp trung bình. Nên điều trị tại Khoa Nội.")

    @Rule(COPDExacerbationFacts(
        pao2=P(lambda pao2: pao2 <= 60),
        paco2=P(lambda paco2: paco2 > 45),
        ph=P(lambda ph: ph >= 7.35)
    ))
    def moderate_exacerbation_with_abg(self):
        self.declare(COPDExacerbationFacts(severity="moderate", treatment_location="internal"))
        print("Chẩn đoán: Đợt cấp trung bình. Nên điều trị tại Khoa Nội.")

    @Rule(COPDExacerbationFacts(
        paco2=P(lambda paco2: paco2 > 45),
        ph=P(lambda ph: ph < 7.35)
    ))
    def severe_exacerbation(self):
        self.declare(COPDExacerbationFacts(severity="severe", treatment_location="icu"))
        print("Chẩn đoán: Đợt cấp nặng. Nên điều trị tại Khoa Hô hấp hoặc Hồi sức tích cực (ICU).")

    @Rule(NOT(COPDExacerbationFacts(severity=W())), salience=-1)
    def unknown_severity(self):
        print("Không đủ thông tin để phân loại đợt cấp. Hãy kiểm tra lại các chỉ số.")

# Sử dụng hệ thống
if __name__ == "__main__":
    engine = COPDExacerbationDiagnosis()
    engine.reset()

    print("Nhập dữ liệu bệnh nhân:")
    vas = int(input("Chỉ số đau (VAS, 0-10): ").strip())
    respiratory_rate = int(input("Tần số thở (lần/phút): ").strip())
    heart_rate = int(input("Nhịp tim (lần/phút): ").strip())
    spo2 = int(input("Độ bão hòa oxy trong máu (%): ").strip())
    crp = int(input("Chỉ số CRP (mg/L): ").strip())
    pao2 = float(input("Áp lực oxy động mạch (mmHg): ").strip())
    paco2 = float(input("Áp lực CO2 động mạch (mmHg): ").strip())
    ph = float(input("Độ pH máu: ").strip())

    engine.declare(COPDExacerbationFacts(
        vas=vas,
        respiratory_rate=respiratory_rate,
        heart_rate=heart_rate,
        spo2=spo2,
        crp=crp,
        pao2=pao2,
        paco2=paco2,
        ph=ph
    ))

    engine.run()

from experta import *

class PatientFacts(Fact):
    """Thông tin bệnh nhân"""
    pass

class COPDExacerbationDiagnosis(KnowledgeEngine):
    
    @Rule(PatientFacts(
        vas=P(lambda vas: vas < 5),
        respiratory_rate=P(lambda rr: rr < 24),
        heart_rate=P(lambda hr: hr < 95),
        spo2=P(lambda spo2: spo2 >= 92),
        crp=P(lambda crp: crp < 10)
    ))
    def mild_exacerbation(self):
        self.declare(Fact(severity="mild"))
        print("Chẩn đoán: Đợt cấp nhẹ. Nên điều trị ngoại trú.")

    @Rule(PatientFacts(
        vas=P(lambda vas: vas >= 5),
        respiratory_rate=P(lambda rr: rr >= 24),
        heart_rate=P(lambda hr: hr >= 95),
        spo2=P(lambda spo2: spo2 < 92),
        crp=P(lambda crp: crp >= 10)
    ))
    def moderate_exacerbation(self):
        self.declare(Fact(severity="moderate"))
        print("Chẩn đoán: Đợt cấp trung bình. Nên điều trị tại Khoa Nội.")

    @Rule(PatientFacts(
        pao2=P(lambda pao2: pao2 <= 60),
        paco2=P(lambda paco2: paco2 > 45),
        ph=P(lambda ph: ph >= 7.35)
    ))
    def moderate_exacerbation_with_abg(self):
        self.declare(Fact(severity="moderate"))
        print("Chẩn đoán: Đợt cấp trung bình. Nên điều trị tại Khoa Nội.")

    @Rule(PatientFacts(
        paco2=P(lambda paco2: paco2 > 45),
        ph=P(lambda ph: ph < 7.35)
    ))
    def severe_exacerbation(self):
        self.declare(Fact(severity="severe"))
        print("Chẩn đoán: Đợt cấp nặng. Nên điều trị tại Khoa Hô hấp hoặc Hồi sức tích cực (ICU).")

    @Rule(NOT(Fact(severity=W())), salience=-1)
    def unknown_severity(self):
        print("Không đủ thông tin để phân loại đợt cấp. Hãy kiểm tra lại các chỉ số.")

# Sử dụng hệ thống
if __name__ == "__main__":
    engine = COPDExacerbationDiagnosis()
    engine.reset()

    # Thêm dữ liệu bệnh nhân
    engine.declare(PatientFacts(vas=6, respiratory_rate=25, heart_rate=96, spo2=91, crp=12))
    engine.run()

from experta import *

class AcuteExacerbationData(Fact):
    """
    Fact lưu trữ thông tin đánh giá độ nặng đợt cấp BPTNMT.
    Các thuộc tính:
    - breathlessness_vas: Điểm khó thở VAS (0-10).
    - respiratory_rate: Tần số thở (lần/phút).
    - heart_rate: Nhịp tim (lần/phút).
    - spo2: SpO2 (%).
    - spo2_drop: Giảm SpO2 (%).
    - crp: CRP (mg/L).
    - pao2: PaO2 (mmHg).
    - paco2: PaCO2 (mmHg).
    - pH: Độ pH trong khí máu động mạch.
    """
    pass

class AcuteExacerbationDiagnosis(KnowledgeEngine):
    @Rule(AcuteExacerbationData(breathlessness_vas=MATCH.vas,
                                respiratory_rate=MATCH.rr,
                                heart_rate=MATCH.hr,
                                spo2=MATCH.spo2,
                                spo2_drop=MATCH.spo2_drop,
                                crp=MATCH.crp),
          TEST(lambda vas, rr, hr, spo2, spo2_drop, crp: vas < 5 and rr < 24 and hr < 95 and spo2 >= 92 and (spo2_drop <= 3 if spo2_drop is not None else True) and (crp < 10 if crp is not None else True)))
    def mild_exacerbation(self):
        print("Chẩn đoán: Đợt cấp nhẹ. Nên điều trị ngoại trú.")

    @Rule(AcuteExacerbationData(breathlessness_vas=MATCH.vas,
                                respiratory_rate=MATCH.rr,
                                heart_rate=MATCH.hr,
                                spo2=MATCH.spo2,
                                spo2_drop=MATCH.spo2_drop,
                                crp=MATCH.crp,
                                pao2=MATCH.pao2,
                                paco2=MATCH.paco2),
          TEST(lambda vas, rr, hr, spo2, spo2_drop, crp, pao2, paco2: sum([vas >= 5, rr >= 24, hr >= 95, spo2 < 92, (spo2_drop > 3 if spo2_drop is not None else False), (crp >= 10 if crp is not None else False)]) >= 3 and (pao2 is None or pao2 <= 60) and (paco2 is None or paco2 > 45)))
    def moderate_exacerbation(self):
        print("Chẩn đoán: Đợt cấp trung bình. Nên điều trị tại Khoa Nội.")

    @Rule(AcuteExacerbationData(paco2=MATCH.paco2, pH=MATCH.pH),
          TEST(lambda paco2, pH: paco2 > 45 and pH < 7.35))
    def severe_exacerbation(self):
        print("Chẩn đoán: Đợt cấp nặng. Nên điều trị tại Khoa Hô hấp hoặc Hồi sức tích cực (ICU).")

if __name__ == "__main__":
    # Tạo instance của hệ thống
    engine = AcuteExacerbationDiagnosis()
    engine.reset()

    # Thu thập dữ liệu từ người dùng
    print("Nhập dữ liệu bệnh nhân:")
    breathlessness_vas = int(input("Điểm khó thở VAS (0-10): ").strip())
    respiratory_rate = int(input("Tần số thở (lần/phút): ").strip())
    heart_rate = int(input("Nhịp tim (lần/phút): ").strip())
    spo2 = float(input("SpO2 (%): ").strip())
    spo2_drop = input("Giảm SpO2 (%, nếu biết): ").strip()
    spo2_drop = float(spo2_drop) if spo2_drop else None
    crp = input("CRP (mg/L, nếu biết): ").strip()
    crp = float(crp) if crp else None
    pao2 = input("PaO2 (mmHg, nếu biết): ").strip()
    pao2 = float(pao2) if pao2 else None
    paco2 = input("PaCO2 (mmHg, nếu biết): ").strip()
    paco2 = float(paco2) if paco2 else None
    pH = input("Độ pH (nếu biết): ").strip()
    pH = float(pH) if pH else None

    # Đưa dữ liệu vào hệ thống
    engine.declare(AcuteExacerbationData(
        breathlessness_vas=breathlessness_vas,
        respiratory_rate=respiratory_rate,
        heart_rate=heart_rate,
        spo2=spo2,
        spo2_drop=spo2_drop,
        crp=crp,
        pao2=pao2,
        paco2=paco2,
        pH=pH
    ))

    # Chạy hệ thống
    engine.run()

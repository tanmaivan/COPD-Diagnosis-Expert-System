from experta import *

class PatientData(Fact):
    """
    Fact lưu trữ thông tin đánh giá chỉ định nội soi can thiệp hoặc phẫu thuật.
    Các thuộc tính:
    - emphysema_severity: Mức độ khí phế thũng (nặng hoặc nhẹ).
    - lobe_hyperinflation: Ứ khí thùy trên (True/False).
    - bode_score: Điểm BODE (0 - 10).
    - acute_CO2_exacerbation: Có đợt cấp với tăng CO2 máu cấp tính (True/False).
    - pulmonary_hypertension: Có tăng áp động mạch phổi (True/False).
    - cor_pulmonale: Có tâm phế mạn (True/False).
    - FEV1: Chỉ số FEV1 (%).
    - DLCO: Chỉ số DLCO (%).
    - emphysema_pattern: Kiểu hình khí phế thũng (đồng nhất hoặc không).
    """
    pass

class InterventionRecommendation(KnowledgeEngine):
    @Rule(PatientData(emphysema_severity="nặng", lobe_hyperinflation=True))
    def recommend_bronchoscopy(self):
        print("Khuyến cáo: Bệnh nhân nên được nội soi can thiệp giảm thể tích phổi để cải thiện khả năng gắng sức, chất lượng cuộc sống và chức năng phổi trong 6-12 tháng.")
        print("Các phương pháp bao gồm: đặt van một chiều, đặt coil hoặc đốt nhiệt.")

    @Rule(PatientData(emphysema_severity="nặng", lobe_hyperinflation=True))
    def recommend_surgery(self):
        print("Khuyến cáo: Phẫu thuật giảm thể tích phổi có thể được chỉ định cho bệnh nhân có ứ khí thùy trên.")

    @Rule(PatientData(bode_score=MATCH.bode_score, emphysema_severity="rất nặng"),
          TEST(lambda bode_score: 7 <= bode_score <= 10),
          OR(Fact(acute_CO2_exacerbation=True),
             Fact(pulmonary_hypertension=True),
             Fact(cor_pulmonale=True),
             AND(Fact(FEV1=MATCH.FEV1, DLCO=MATCH.DLCO, emphysema_pattern="đồng nhất"),
                 TEST(lambda FEV1, DLCO: FEV1 < 20 and DLCO < 20))))
    def recommend_lung_transplant(self):
        print("Khuyến cáo: Bệnh nhân có thể được chỉ định ghép phổi.")
        print("Tiêu chí gồm: tiền sử đợt cấp với tăng CO2 máu cấp tính (PaCO2 > 50mmHg), tăng áp động mạch phổi và/hoặc tâm phế mạn dù đã thở oxy, hoặc FEV1 < 20% và DLCO < 20% với kiểu hình khí phế thũng đồng nhất.")

if __name__ == "__main__":
    # Tạo instance của hệ thống
    engine = InterventionRecommendation()
    engine.reset()

    # Thu thập dữ liệu từ người dùng
    print("Nhập dữ liệu bệnh nhân:")
    emphysema_severity = input("Mức độ khí phế thũng (nặng/rất nặng): ").strip()
    lobe_hyperinflation = input("Bệnh nhân có ứ khí thùy trên không? (True/False): ").strip().lower() == "true"
    bode_score = int(input("Điểm BODE (0-10): ").strip())
    acute_CO2_exacerbation = input("Có đợt cấp với tăng CO2 máu cấp tính không? (True/False): ").strip().lower() == "true"
    pulmonary_hypertension = input("Có tăng áp động mạch phổi không? (True/False): ").strip().lower() == "true"
    cor_pulmonale = input("Có tâm phế mạn không? (True/False): ").strip().lower() == "true"
    FEV1 = int(input("Chỉ số FEV1 (%): ").strip())
    DLCO = int(input("Chỉ số DLCO (%): ").strip())
    emphysema_pattern = input("Kiểu hình khí phế thũng (đồng nhất/không): ").strip()

    # Đưa dữ liệu vào hệ thống
    engine.declare(PatientData(
        emphysema_severity=emphysema_severity,
        lobe_hyperinflation=lobe_hyperinflation,
        bode_score=bode_score,
        acute_CO2_exacerbation=acute_CO2_exacerbation,
        pulmonary_hypertension=pulmonary_hypertension,
        cor_pulmonale=cor_pulmonale,
        FEV1=FEV1,
        DLCO=DLCO,
        emphysema_pattern=emphysema_pattern
    ))

    # Chạy hệ thống
    engine.run()

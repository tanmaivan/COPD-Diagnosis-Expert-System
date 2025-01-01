from experta import *

# Hệ thống chẩn đoán và lựa chọn kháng sinh
class Outpatient(Fact):
    """
    Thông tin bệnh nhân:
    - breathlessness_increase: Khó thở tăng (True/False).
    - sputum_volume_or_thickness_increase: Thể tích hoặc độ quánh đờm tăng (True/False).
    - purulent_sputum_increase: Đờm mủ tăng (True/False).
    - fev1: Chỉ số FEV1 (%).
    - exacerbations: Số đợt cấp BPTNMT trong 12 tháng qua.
    - hospitalization: Nhập viện vì đợt cấp BPTNMT trong 3 tháng qua (True/False).
    - risk_oxygen_home: Đang dùng liệu pháp oxy dài hạn tại nhà (True/False).
    - risk_comorbidities: Có bệnh đồng mắc (True/False).
    - risk_pseudomonas: Có nguy cơ nhiễm Pseudomonas (True/False).
    - gian_phe_quan: Giãn phế quang trên X-quang hoặc CT ngực (True/False).
    - dung_khang_sinh_pho_rong: Có dùng kháng sinh phổ rộng (True/False).
    """
    breathlessness_increase = Field(bool)
    sputum_volume_or_thickness_increase = Field(bool)
    purulent_sputum_increase = Field(bool)
    fev1 = Field(float)
    exacerbations = Field(int)
    hospitalization = Field(bool)
    risk_oxygen_home = Field(bool)
    risk_comorbidities = Field(bool)
    risk_pseudomonas = Field(bool)
    gian_phe_quan = Field(bool)
    dung_khang_sinh_pho_rong = Field(bool)

class EmpiricalAntibioticSelectionOutpatient(KnowledgeEngine):
    def __init__(self):
        super().__init__()
        self.result = ""

    @Rule(Outpatient(symptom_main_1=False, symptom_main_2=False, symptom_main_3=False))
    def stage_1_no_antibiotics(self):
        self.result = "Kháng sinh không được chỉ định trừ khi triệu chứng đã xấu hơn dù đã điều trị hỗ trợ phù hợp."
        print(self.result)

    @Rule(Outpatient(symptom_main_1=True, symptom_main_2=True))
    @Rule(Outpatient(symptom_main_1=True, symptom_main_3=True))
    @Rule(Outpatient(symptom_main_2=True, symptom_main_3=True))
    def stage_1_proceed(self):
        print("Có đủ triệu chứng chính. Chuyển sang giai đoạn 2.")

    @Rule(Outpatient(fev1=MATCH.fev1, exacerbations=MATCH.exacerbations, hospitalization=False,
                  risk_oxygen_home=False, risk_comorbidities=False))
    def stage_2_low_risk(self, fev1, exacerbations):
        if fev1 >= 50 and exacerbations < 2:
            self.result = "Tùy thuộc đặc điểm bệnh nhân, chọn 1 trong các kháng sinh sau:\n- Macrolide\n- Cephalosporin thế hệ 2 hoặc 3"
            print(self.result)

    @Rule(Outpatient(fev1=MATCH.fev1, exacerbations=MATCH.exacerbations) & (
          Outpatient(hospitalization=True) | Outpatient(risk_oxygen_home=True) |
          Outpatient(risk_comorbidities=True)))
    def stage_2_high_risk(self, fev1, exacerbations):
        if fev1 < 50 or exacerbations >= 2:
            self.result = "Có yếu tố nguy cơ kết cục xấu. Chuyển sang giai đoạn 3."
            print(self.result)

    @Rule(Outpatient(risk_pseudomonas=True))
    def stage_3_pseudomonas(self):
        self.result = "Điều trị bằng ciprofloxacine và cấy đờm làm kháng sinh."
        print(self.result)

    @Rule(Outpatient(risk_pseudomonas=False))
    def stage_3_proceed(self):
        print("Không có nguy cơ nhiễm Pseudomonas. Chuyển sang giai đoạn 4.")

    @Rule(Outpatient(fev1=MATCH.fev1, gian_phe_quan=MATCH.gian_phe_quan, dung_khang_sinh_pho_rong=MATCH.dung_khang_sinh_pho_rong))
    def stage_4(self, fev1, gian_phe_quan, dung_khang_sinh_pho_rong):
        if fev1 < 30 or gian_phe_quan or dung_khang_sinh_pho_rong:
            self.result = "Điều trị bằng ciprofloxacin hoặc levofloxacin và cấy đờm làm kháng sinh đồ."
        else:
            self.result = "Tùy thuộc đặc điểm bệnh nhân, chọn 1 trong các kháng sinh sau:\n- Amoxicillin-clavulanate\n- Levofloxacin hoặc moxifloxacin"
        print(self.result)

# Hệ thống thực thi
def main():
    engine = EmpiricalAntibioticSelectionOutpatient()
    engine.reset()

    # Giai đoạn 1: Nhập triệu chứng chính
    print("Nhập các triệu chứng chính:")
    symptom_main_1 = input("Khó thở tăng (True/False): ").lower() == "true"
    symptom_main_2 = input("Thể tích hoặc độ quánh đờm tăng (True/False): ").lower() == "true"
    symptom_main_3 = input("Đờm mủ tăng (True/False): ").lower() == "true"

    engine.declare(Outpatient(symptom_main_1=symptom_main_1, symptom_main_2=symptom_main_2, symptom_main_3=symptom_main_3))
    engine.run()

    if engine.result:
        return

    # Giai đoạn 2: Nhập yếu tố nguy cơ
    print("\nNhập các yếu tố nguy cơ:")
    fev1 = float(input("FEV1: "))
    exacerbations = int((input("Số đợt cấp BPTNMT trong 12 tháng qua: ")) or 0)
    hospitalization = input("Nhập viện vì đợt cấp BPTNMT trong 3 tháng qua (True/False): ").lower() == "true"
    risk_oxygen_home = input("Đang dùng liệu pháp oxy dài hạn tại nhà (True/False): ").lower() == "true"
    risk_comorbidities = input("Có bệnh đồng mắc (True/False): ").lower() == "true"

    engine.declare(Outpatient(fev1=fev1, exacerbations=exacerbations,
                           hospitalization=hospitalization, risk_oxygen_home=risk_oxygen_home,
                           risk_comorbidities=risk_comorbidities))
    engine.run()

    if engine.result:
        return

    # Giai đoạn 3: Kiểm tra nguy cơ nhiễm Pseudomonas
    print("\nKiểm tra nguy cơ nhiễm Pseudomonas:")
    risk_pseudomonas = input("Có nguy cơ nhiễm Pseudomonas (True/False): ").lower() == "true"

    engine.declare(Outpatient(risk_pseudomonas=risk_pseudomonas))
    engine.run()

    if engine.result:
        return

    # Giai đoạn 4: Kiểm tra yếu tố nguy cơ khác gây nhiễm Pseudomonas
    print("\nKiểm tra yếu tố nguy cơ khác:")
    
    # Nhập gian_phe_quan hoặc dung_khang_sinh_pho_rong
    gian_phe_quan = input("Giãn phế quang trên X-quang hoặc CT ngực (True/False): ").lower() == "true"
    dung_khang_sinh_pho_rong = input("Có dùng kháng sinh phổ rộng (True/False): ").lower() == "true"

    # Khai báo các yếu tố nguy cơ khác
    engine.declare(Patient(fev1=fev1,gian_phe_quan=gian_phe_quan, dung_khang_sinh_pho_rong=dung_khang_sinh_pho_rong))
    engine.run()

if __name__ == "__main__":
    main()

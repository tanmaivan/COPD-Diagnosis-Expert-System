from experta import *

# Hệ thống chẩn đoán và lựa chọn kháng sinh
class Patient(Fact):
    """Thông tin bệnh nhân"""
    pass

class ExacerbationAntibioticsExpert(KnowledgeEngine):
    def __init__(self):
        super().__init__()
        self.result = ""

    @Rule(Patient(symptom_main_1=False, symptom_main_2=False, symptom_main_3=False))
    def stage_1_no_antibiotics(self):
        self.result = "Kháng sinh không được chỉ định trừ khi triệu chứng đã xấu hơn dù đã điều trị hỗ trợ phù hợp."
        print(self.result)

    @Rule(Patient(symptom_main_1=True, symptom_main_2=True))
    @Rule(Patient(symptom_main_1=True, symptom_main_3=True))
    @Rule(Patient(symptom_main_2=True, symptom_main_3=True))
    def stage_1_proceed(self):
        print("Có đủ triệu chứng chính. Chuyển sang giai đoạn 2.")

    @Rule(Patient(risk_fev1_lt_50=False, risk_exacerbations_lt_2=False, risk_hospitalization_3m=False,
                  risk_oxygen_home=False, risk_comorbidities=False))
    def stage_2_low_risk(self):
        self.result = "Tùy thuộc đặc điểm bệnh nhân, chọn 1 trong các kháng sinh sau:\n- Macrolide\n- Cephalosporin thế hệ 2 hoặc 3"
        print(self.result)

    @Rule(Patient(risk_fev1_lt_50=True) | Patient(risk_exacerbations_lt_2=False) |
          Patient(risk_hospitalization_3m=True) | Patient(risk_oxygen_home=True) |
          Patient(risk_comorbidities=True))
    def stage_2_high_risk(self):
        print("Có yếu tố nguy cơ kết cục xấu. Chuyển sang giai đoạn 3.")

    @Rule(Patient(risk_pseudomonas=True))
    def stage_3_pseudomonas(self):
        self.result = "Điều trị bằng ciprofloxacine và cấy đờm làm kháng sinh đồ."
        print(self.result)

    @Rule(Patient(risk_pseudomonas=False))
    def stage_3_proceed(self):
        print("Không có nguy cơ nhiễm Pseudomonas. Chuyển sang giai đoạn 4.")

class ExacerbationAntibioticsExpert(KnowledgeEngine):
    @Rule(Patient(fev1=MATCH.fev1, gian_phe_quan=MATCH.gian_phe_quan, dung_khang_sinh_pho_rong=MATCH.dung_khang_sinh_pho_rong))
    def stage_4(self, fev1, gian_phe_quan, dung_khang_sinh_pho_rong):
        if fev1 < 30 or gian_phe_quan or dung_khang_sinh_pho_rong:
            self.result = "Điều trị bằng ciprofloxacin hoặc levofloxacin và cấy đờm làm kháng sinh đồ."
        else:
            self.result = "Tùy thuộc đặc điểm bệnh nhân, chọn 1 trong các kháng sinh sau:\n- Amoxicillin-clavulanate\n- Levofloxacin hoặc moxifloxacin"
        print(self.result)

# Hệ thống thực thi
def main():
    engine = ExacerbationAntibioticsExpert()
    engine.reset()

    # Giai đoạn 1: Nhập triệu chứng chính
    print("Nhập các triệu chứng chính:")
    symptom_main_1 = input("Khó thở tăng (True/False): ").lower() == "true"
    symptom_main_2 = input("Thể tích hoặc độ quánh đờm tăng (True/False): ").lower() == "true"
    symptom_main_3 = input("Đờm mủ tăng (True/False): ").lower() == "true"

    engine.declare(Patient(symptom_main_1=symptom_main_1, symptom_main_2=symptom_main_2, symptom_main_3=symptom_main_3))
    engine.run()

    if engine.result:
        return

    # Giai đoạn 2: Nhập yếu tố nguy cơ
    print("\nNhập các yếu tố nguy cơ:")
    risk_fev1_lt_50 = input("FEV1 < 50% (True/False): ").lower() == "true"
    risk_exacerbations_lt_2 = input(">=2 đợt cấp BPTNMT trong 12 tháng qua (True/False): ").lower() == "true"
    risk_hospitalization_3m = input("Nhập viện vì đợt cấp BPTNMT trong 3 tháng qua (True/False): ").lower() == "true"
    risk_oxygen_home = input("Đang dùng liệu pháp oxy dài hạn tại nhà (True/False): ").lower() == "true"
    risk_comorbidities = input("Có bệnh đồng mắc (True/False): ").lower() == "true"

    engine.declare(Patient(risk_fev1_lt_50=risk_fev1_lt_50, risk_exacerbations_lt_2=risk_exacerbations_lt_2,
                           risk_hospitalization_3m=risk_hospitalization_3m, risk_oxygen_home=risk_oxygen_home,
                           risk_comorbidities=risk_comorbidities))
    engine.run()

    if engine.result:
        return

    # Giai đoạn 3: Kiểm tra nguy cơ nhiễm Pseudomonas
    print("\nKiểm tra nguy cơ nhiễm Pseudomonas:")
    risk_pseudomonas = input("Có nguy cơ nhiễm Pseudomonas (True/False): ").lower() == "true"

    engine.declare(Patient(risk_pseudomonas=risk_pseudomonas))
    engine.run()

    if engine.result:
        return

    # Giai đoạn 4: Kiểm tra yếu tố nguy cơ khác gây nhiễm Pseudomonas
    print("\nKiểm tra yếu tố nguy cơ khác:")
    risk_pseudomonas_other = input("Có yếu tố nguy cơ khác gây nhiễm Pseudomonas (True/False): ").lower() == "true"

    engine.declare(Patient(risk_pseudomonas_other=risk_pseudomonas_other))
    engine.run()

if __name__ == "__main__":
    main()

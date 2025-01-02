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
    - bronchiectasis: Giãn phế quang trên X-quang hoặc CT ngực (True/False).
    - broad_spectrum_antibiotic_use: Có dùng kháng sinh phổ rộng (True/False).
    - antibiotic_selection: Lựa chọn kháng sinh
    - antibiotic_selection_description: Mô tả lựa chọn kháng sinh.
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
    bronchiectasis = Field(bool)
    broad_spectrum_antibiotic_use = Field(bool)
    antibiotic_selection_description = Field(str)

class EmpiricalAntibioticSelectionOutpatient(KnowledgeEngine):
    def __init__(self):
        super().__init__()
        self.stage_1_proceeded = False
        self.stage_2_proceeded = False
        self.result = ""
        self.flag = False

    @Rule(Outpatient(breathlessness_increase=False, sputum_volume_or_thickness_increase=False, purulent_sputum_increase=False) | Outpatient(breathlessness_increase=True, sputum_volume_or_thickness_increase=False, purulent_sputum_increase=False) | Outpatient(breathlessness_increase=False, sputum_volume_or_thickness_increase=True, purulent_sputum_increase=False) | Outpatient(breathlessness_increase=False, sputum_volume_or_thickness_increase=False, purulent_sputum_increase=True))
    def stage_1_no_antibiotics(self):
        self.result = "Kháng sinh không được chỉ định trừ khi triệu chứng đã xấu hơn dù đã điều trị hỗ trợ phù hợp."
        print(self.result)
        self.declare(Outpatient(antibiotic_selection_description=self.result))
        self.flag = True

    @Rule(Outpatient(breathlessness_increase=True, sputum_volume_or_thickness_increase=True)| Outpatient(breathlessness_increase=True, purulent_sputum_increase=True) | Outpatient(sputum_volume_or_thickness_increase=True, purulent_sputum_increase=True))
    def stage_1_proceed(self):
        if not self.stage_1_proceeded:
            self.stage_1_proceeded = True
            self.result = "Có đủ triệu chứng chính. Chuyển sang giai đoạn 2."
            print(self.result)
            self.declare(Outpatient(antibiotic_selection_description=self.result))
        
    @Rule(Outpatient(fev1=MATCH.fev1, exacerbations=MATCH.exacerbations, hospitalization=False,
                  risk_oxygen_home=False, risk_comorbidities=False))
    def stage_2_low_risk(self, fev1, exacerbations):
        if fev1 >= 50 and exacerbations < 2:
            self.result = "Tùy thuộc đặc điểm bệnh nhân, chọn 1 trong các kháng sinh sau:\n- Macrolide\n- Cephalosporin thế hệ 2 hoặc 3"
            print(self.result)
            self.declare(Outpatient(antibiotic_selection_description=self.result))
            self.flag = True

    @Rule(Outpatient(fev1=MATCH.fev1, exacerbations=MATCH.exacerbations, hospitalization=MATCH.hospitalization, risk_oxygen_home=MATCH.risk_oxygen_home, risk_comorbidities=MATCH.risk_comorbidities))
    def stage_2_high_risk(self, fev1, exacerbations, hospitalization, risk_oxygen_home, risk_comorbidities):
        if fev1 < 50 or exacerbations >= 2 or hospitalization or risk_oxygen_home or risk_comorbidities:
            if not self.stage_2_proceeded:
                self.stage_2_proceeded = True
                self.result = "Có yếu tố nguy cơ kết cục xấu. Chuyển sang giai đoạn 3."
                print(self.result)
                self.declare(Outpatient(antibiotic_selection_description=self.result))

    @Rule(Outpatient(risk_pseudomonas=True))
    def stage_3_pseudomonas(self):
        self.result = "Điều trị bằng ciprofloxacine và cấy đờm làm kháng sinh."
        print(self.result)
        self.declare(Outpatient(antibiotic_selection_description=self.result))
        self.flag = True

    @Rule(Outpatient(risk_pseudomonas=False))
    def stage_3_proceed(self):
        self.result = "Không có nguy cơ nhiễm Pseudomonas. Chuyển sang giai đoạn 4."
        print(self.result)
        self.declare(Outpatient(antibiotic_selection_description=self.result))

    @Rule(Outpatient(fev1=MATCH.fev1, bronchiectasis=MATCH.bronchiectasis, broad_spectrum_antibiotic_use=MATCH.broad_spectrum_antibiotic_use))
    def stage_4(self, fev1, bronchiectasis, broad_spectrum_antibiotic_use):
        if fev1 < 30 or bronchiectasis or broad_spectrum_antibiotic_use:
            self.result = "Điều trị bằng ciprofloxacin hoặc levofloxacin và cấy đờm làm kháng sinh đồ."
        else:
            self.result = "Tùy thuộc đặc điểm bệnh nhân, chọn 1 trong các kháng sinh sau:\n- Amoxicillin-clavulanate\n- Levofloxacin hoặc moxifloxacin"
        print(self.result)
        self.declare(Outpatient(antibiotic_selection_description=self.result))
        self.flag = True

# Hệ thống thực thi
def main():
    engine_1 = EmpiricalAntibioticSelectionOutpatient()
    engine_2 = EmpiricalAntibioticSelectionOutpatient()
    engine_3 = EmpiricalAntibioticSelectionOutpatient()
    engine_4 = EmpiricalAntibioticSelectionOutpatient()
    engine_1.reset()
    engine_2.reset()
    engine_3.reset()
    engine_4.reset()

    # Giai đoạn 1: Nhập triệu chứng chính
    print("Nhập các triệu chứng chính:")
    breathlessness_increase = input("Khó thở tăng (True/False): ").lower() == "true"
    sputum_volume_or_thickness_increase = input("Thể tích hoặc độ quánh đờm tăng (True/False): ").lower() == "true"
    purulent_sputum_increase = input("Đờm mủ tăng (True/False): ").lower() == "true"

    engine_1.declare(Outpatient(breathlessness_increase=breathlessness_increase, sputum_volume_or_thickness_increase=sputum_volume_or_thickness_increase, purulent_sputum_increase=purulent_sputum_increase))
    engine_1.run()

    for fact_id, fact in engine_1.facts.items():   
        print(f"Fact ID: {fact_id}")
        for key, value in fact.items():
            print(f"{key}: {value}")
    
    if engine_1.flag:
        return

    # Giai đoạn 2: Nhập yếu tố nguy cơ
    print("\nNhập các yếu tố nguy cơ:")
    fev1 = float(input("FEV1: "))
    exacerbations = int((input("Số đợt cấp BPTNMT trong 12 tháng qua: ")) or 0)
    hospitalization = input("Nhập viện vì đợt cấp BPTNMT trong 3 tháng qua (True/False): ").lower() == "true"
    risk_oxygen_home = input("Đang dùng liệu pháp oxy dài hạn tại nhà (True/False): ").lower() == "true"
    risk_comorbidities = input("Có bệnh đồng mắc (True/False): ").lower() == "true"

    engine_2.declare(Outpatient(fev1=fev1, exacerbations=exacerbations,
                           hospitalization=hospitalization, risk_oxygen_home=risk_oxygen_home,
                           risk_comorbidities=risk_comorbidities))
    engine_2.run()

    for fact_id, fact in engine_2.facts.items():   
        print(f"Fact ID: {fact_id}")
        for key, value in fact.items():
            print(f"{key}: {value}")

    if engine_2.flag:
        return

    # Giai đoạn 3: Kiểm tra nguy cơ nhiễm Pseudomonas
    print("\nKiểm tra nguy cơ nhiễm Pseudomonas:")
    risk_pseudomonas = input("Có nguy cơ nhiễm Pseudomonas (True/False): ").lower() == "true"

    engine_3.declare(Outpatient(risk_pseudomonas=risk_pseudomonas))
    engine_3.run()

    for fact_id, fact in engine_3.facts.items():   
        print(f"Fact ID: {fact_id}")
        for key, value in fact.items():
            print(f"{key}: {value}")

    if engine_3.flag:
        return
    

    # Giai đoạn 4: Kiểm tra yếu tố nguy cơ khác gây nhiễm Pseudomonas
    print("\nKiểm tra yếu tố nguy cơ khác:")
    
    # Nhập bronchiectasis hoặc broad_spectrum_antibiotic_use
    bronchiectasis = input("Giãn phế quang trên X-quang hoặc CT ngực (True/False): ").lower() == "true"
    broad_spectrum_antibiotic_use = input("Có dùng kháng sinh phổ rộng (True/False): ").lower() == "true"

    # Khai báo các yếu tố nguy cơ khác
    engine_4.declare(Outpatient(fev1=fev1,bronchiectasis=bronchiectasis, broad_spectrum_antibiotic_use=broad_spectrum_antibiotic_use))
    engine_4.run()

    for fact_id, fact in engine_4.facts.items():   
        print(f"Fact ID: {fact_id}")
        for key, value in fact.items():
            print(f"{key}: {value}")

if __name__ == "__main__":
    main()

from experta import *

class Inpatient(Fact):
    """
    Thông tin bệnh nhân:
    - suspect_pneumonia_or_infection: Bệnh nhân có nghi ngờ viêm phổi hoặc nhiễm khuẩn nơi khác? (True/False)
    - risk_pseudomonas: Bệnh nhân có yếu tố nguy cơ nhiễm Pseudomonas? (True/False)
    - antibiotic_selection: Lựa chọn kháng sinh
    """
    suspect_pneumonia_or_infection = Field(bool)
    risk_pseudomonas = Field(bool)
    antibiotic_selection_description = Field(str)

class EmpiricalAntibioticSelectionInpatient(KnowledgeEngine):
    def __init__(self):
        super().__init__()
        self.result = ""
        self.flag = False

    # Giai đoạn 1: Nghi ngờ viêm phổi hoặc nhiễm khuẩn nơi khác
    @Rule(Inpatient(suspect_pneumonia_or_infection=True))
    def stage_1_treat_infection(self):
        self.result = "Đánh giá và điều trị viêm phổi và/hoặc nhiễm khuẩn nơi khác."
        print(self.result)
        self.declare(Inpatient(antibiotic_selection_description=self.result))
        self.flag = True

    @Rule(Inpatient(suspect_pneumonia_or_infection=False))
    def stage_1_no_infection(self):
        self.result = "Không nghi ngờ viêm phổi hoặc nhiễm khuẩn nơi khác. Chuyển sang giai đoạn 2."
        print(self.result)
        self.declare(Inpatient(antibiotic_selection_description=self.result))

    # Giai đoạn 2: Có yếu tố nguy cơ nhiễm Pseudomonas
    @Rule(Inpatient(risk_pseudomonas=True))
    def stage_2_pseudomonas(self):
        self.result = "Nhuộm Gram và cấy đờm làm kháng sinh đồ, chọn 1 trong các kháng sinh diệt Pseudomonas:\n-	Ciprofloxacin\n-	Cefepime\n-	Ceftazidime\n-	Piperacillin-tazobactam\n-	Carbapemen nhóm 2\n"
        print(self.result)
        self.declare(Inpatient(antibiotic_selection_description=self.result))

    @Rule(Inpatient(risk_pseudomonas=False))
    def stage_2_no_pseudomonas(self):
        self.result = "Nhuộm Gram và cấy đờm làm kháng sinh đồ, chọn kháng sinh theo kinh nghiệm dựa vào đặc điểm bệnh nhân, tính nhạy cảm kháng sinh tại địa phương, tiền sử dùng kháng sinh:\n-	Một fluoroquinolone hô hấp (levofloxacin hoặc moxifloxacin) HOẶC\n-	Một cephalosporin thế hệ 3 (ceftriaxone hoặc cefotaxime)\n"
        print(self.result)
        self.declare(Inpatient(antibiotic_selection_description=self.result))

def main():
    engine_1 = EmpiricalAntibioticSelectionInpatient()
    engine_1.reset()

    engine_2 = EmpiricalAntibioticSelectionInpatient()
    engine_2.reset()

    suspect_pneumonia_or_infection = input("Bệnh nhân có nghi ngờ viêm phổi hoặc nhiễm khuẩn nơi khác? (True/False): ").strip().lower() == "true"

    engine_1.declare(Inpatient(suspect_pneumonia_or_infection=suspect_pneumonia_or_infection))
    engine_1.run()

    if engine_1.flag:
        return

    risk_pseudomonas = input("Bệnh nhân có yếu tố nguy cơ nhiễm Pseudomonas? (True/False): ").strip().lower() == "true"

    engine_2.declare(Inpatient(risk_pseudomonas=risk_pseudomonas))
    engine_2.run()

if __name__ == "__main__":
    main()
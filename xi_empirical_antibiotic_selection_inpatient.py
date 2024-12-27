from experta import *

class Inpatient(Fact):
    """
    Thông tin bệnh nhân:
    - suspect_pneumonia_or_infection: Bệnh nhân có nghi ngờ viêm phổi hoặc nhiễm khuẩn nơi khác? (True/False)
    - risk_pseudomonas: Bệnh nhân có yếu tố nguy cơ nhiễm Pseudomonas? (True/False)
    """
    suspect_pneumonia_or_infection = Field(bool)
    risk_pseudomonas = Field(bool)

class EmpiricalAntibioticSelectionInpatient(KnowledgeEngine):
    def __init__(self):
        super().__init__()
        self.result = ""

    # Giai đoạn 1: Nghi ngờ viêm phổi hoặc nhiễm khuẩn nơi khác
    @Rule(Inpatient(suspect_pneumonia_or_infection=True))
    def stage_1_treat_infection(self):
        self.result = "Đánh giá và điều trị viêm phổi và/hoặc nhiễm khuẩn nơi khác."
        print(self.result)

    @Rule(Inpatient(suspect_pneumonia_or_infection=False))
    def stage_1_no_infection(self):
        print("Không nghi ngờ viêm phổi hoặc nhiễm khuẩn nơi khác. Chuyển sang giai đoạn 2.")

    # Giai đoạn 2: Có yếu tố nguy cơ nhiễm Pseudomonas
    @Rule(Inpatient(risk_pseudomonas=True))
    def stage_2_pseudomonas(self):
        self.result = "Nhuộm Gram và cấy đờm làm kháng sinh đồ, chọn 1 trong các kháng sinh diệt Pseudomonas:\n-	Ciprofloxacin\n-	Cefepime\n-	Ceftazidime\n-	Piperacillin-tazobactam\n-	Carbapemen nhóm 2\n"
        print(self.result)

    @Rule(Inpatient(risk_pseudomonas=False))
    def stage_2_no_pseudomonas(self):
        self.result = "Nhuộm Gram và cấy đờm làm kháng sinh đồ, chọn kháng sinh theo kinh nghiệm dựa vào đặc điểm bệnh nhân, tính nhạy cảm kháng sinh tại địa phương, tiền sử dùng kháng sinh:\n-	Một fluoroquinolone hô hấp (levofloxacin hoặc moxifloxacin) HOẶC\n-	Một cephalosporin thế hệ 3 (ceftriaxone hoặc cefotaxime)\n"
        print(self.result)

def main():
    engine = EmpiricalAntibioticSelectionInpatient()
    engine.reset()

    suspect_pneumonia_or_infection = input("Bệnh nhân có nghi ngờ viêm phổi hoặc nhiễm khuẩn nơi khác? (True/False): ").strip().lower() == "true"

    engine.declare(Inpatient(suspect_pneumonia_or_infection=suspect_pneumonia_or_infection))
    engine.run()

    if engine.result:
        return

    risk_pseudomonas = input("Bệnh nhân có yếu tố nguy cơ nhiễm Pseudomonas? (True/False): ").strip().lower() == "true"

    engine.declare(Inpatient(risk_pseudomonas=risk_pseudomonas))
    engine.run()

if __name__ == "__main__":
    main()
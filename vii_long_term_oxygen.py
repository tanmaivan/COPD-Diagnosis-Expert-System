from experta import *

class OxygenAssessment(Fact):
    """
    OxygenAssessment lưu trữ thông tin về chỉ số oxy và các dấu hiệu liên quan.
    Các thuộc tính:
    - PaO2: Áp lực oxy động mạch (mmHg).
    - SaO2: Độ bão hòa oxy máu (%).
    - heart_failure: Có dấu hiệu suy tim phải (True/False).
    - polycythemia: Đa hồng cầu, hematocrit > 55% (True/False).
    - pulmonary_hypertension: Tăng áp động mạch phổi (True/False).
    - oxygen_required: Cần thở oxy dài hạn tại nhà (True/False).
    - long_term_oxygen_reason: Nguyên nhân cần thở oxy
    """
    PaO2 = Field(float)
    SaO2 = Field(float)
    heart_failure = Field(bool)
    polycythemia = Field(bool)
    pulmonary_hypertension = Field(bool)
    oxygen_required = Field(bool)
    long_term_oxygen_reason = Field(list)

class OxygenTherapyEngine(KnowledgeEngine):
    def __init__(self):
        super().__init__()
        self.oxygen_required = False
        self.long_term_oxygen_reason = []

    @Rule(OxygenAssessment(PaO2=MATCH.PaO2, SaO2=MATCH.SaO2, heart_failure=False, polycythemia=False, pulmonary_hypertension=False),
          TEST(lambda PaO2, SaO2: PaO2 > 59 and SaO2 > 88))
    def no_oxygen_needed(self):
        result = "Bệnh nhân không suy hô hấp mạn tính, thiếu oxy máu."
        self.long_term_oxygen_reason.append(result)
        self.declare(OxygenAssessment(oxygen_required=False,long_term_oxygen_reason=self.long_term_oxygen_reason))

    @Rule(OxygenAssessment(PaO2=MATCH.PaO2, SaO2=MATCH.SaO2),
          TEST(lambda PaO2, SaO2: PaO2 <= 55 or SaO2 <= 88))
    def oxygen_needed_low_levels(self):
        self.oxygen_required = True
        result = "- Mức PaO₂ dưới 55 hoặc SaO₂ dưới 88."
        self.long_term_oxygen_reason.append(result)

    @Rule(OxygenAssessment(PaO2=MATCH.PaO2, SaO2=MATCH.SaO2, heart_failure=True),
          TEST(lambda PaO2, SaO2: 56 <= PaO2 <= 59 or SaO2 <= 88))
    def oxygen_needed_with_heart_failure(self):
        self.oxygen_required = True
        result = "- PaO₂ hoặc SaO₂ thấp kèm dấu hiệu suy tim phải."
        self.long_term_oxygen_reason.append(result)

    @Rule(OxygenAssessment(PaO2=MATCH.PaO2, SaO2=MATCH.SaO2, polycythemia=True),
          TEST(lambda PaO2, SaO2: 56 <= PaO2 <= 59 or SaO2 <= 88))
    def oxygen_needed_with_polycythemia(self):
        self.oxygen_required = True
        result = "- PaO₂ hoặc SaO₂ thấp kèm đa hồng cầu."
        self.long_term_oxygen_reason.append(result)

    @Rule(OxygenAssessment(PaO2=MATCH.PaO2, SaO2=MATCH.SaO2, pulmonary_hypertension=True),
          TEST(lambda PaO2, SaO2: 56 <= PaO2 <= 59 or SaO2 <= 88))
    def oxygen_needed_with_pulmonary_hypertension(self):
        self.oxygen_required = True
        result = "- PaO₂ hoặc SaO₂ thấp kèm tăng áp động mạch phổi."
        self.long_term_oxygen_reason.append(result)

    @Rule(OxygenAssessment(), salience=-1)
    def check_oxygen_required(self):
        if self.oxygen_required:
            self.declare(OxygenAssessment(oxygen_required=True, long_term_oxygen_reason=self.long_term_oxygen_reason))

if __name__ == "__main__":
    engine = OxygenTherapyEngine()

    engine.reset()

    PaO2 = float(input("Nhập PaO2 (mmHg): "))
    SaO2 = float(input("Nhập SaO2 (%): "))
    heart_failure = input("Bệnh nhân có dấu hiệu suy tim phải? (True/False): ").strip().lower() == "true"
    polycythemia = input("Bệnh nhân có đa hồng cầu (hematocrit > 55%)? (True/False): ").strip().lower() == "true"
    pulmonary_hypertension = input("Bệnh nhân có tăng áp động mạch phổi? (True/False): ").strip().lower() == "true"

    engine.declare(OxygenAssessment(PaO2=PaO2, SaO2=SaO2, heart_failure=heart_failure,
                                        polycythemia=polycythemia, pulmonary_hypertension=pulmonary_hypertension))

    engine.run()

    for fact_id, fact in engine.facts.items():   
        print(f"Fact ID: {fact_id}")
        for key, value in fact.items():
            print(f"{key}: {value}")

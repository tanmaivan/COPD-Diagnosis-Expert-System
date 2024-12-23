from experta import *

class OxygenAssessment(Fact):
    """
    Fact lưu trữ thông tin về chỉ số oxy và các dấu hiệu liên quan.
    Các thuộc tính:
    - PaO2: Áp lực oxy động mạch (mmHg).
    - SaO2: Độ bão hòa oxy máu (%).
    - heart_failure: Có dấu hiệu suy tim phải (True/False).
    - polycythemia: Đa hồng cầu, hematocrit > 55% (True/False).
    - pulmonary_hypertension: Tăng áp động mạch phổi (True/False).
    """
    pass

class OxygenTherapyEngine(KnowledgeEngine):
    @Rule(OxygenAssessment(PaO2=MATCH.PaO2, SaO2=MATCH.SaO2, heart_failure=False, polycythemia=False, pulmonary_hypertension=False),
          TEST(lambda PaO2, SaO2: PaO2 > 59 and SaO2 > 88))
    def no_oxygen_needed(self):
        self.declare(Fact(oxygen_required=False))
        print("Bệnh nhân không cần thở oxy dài hạn tại nhà.")

    @Rule(OxygenAssessment(PaO2=MATCH.PaO2, SaO2=MATCH.SaO2),
          TEST(lambda PaO2, SaO2: PaO2 <= 55 or SaO2 <= 88))
    def oxygen_needed_low_levels(self):
        self.declare(Fact(oxygen_required=True))
        print("Bệnh nhân cần thở oxy dài hạn tại nhà (do mức PaO2 hoặc SaO2 thấp).")

    @Rule(OxygenAssessment(PaO2=MATCH.PaO2, SaO2=MATCH.SaO2, heart_failure=True),
          TEST(lambda PaO2, SaO2: 56 <= PaO2 <= 59 or SaO2 <= 88))
    def oxygen_needed_with_heart_failure(self):
        self.declare(Fact(oxygen_required=True))
        print("Bệnh nhân cần thở oxy dài hạn tại nhà (do PaO2 hoặc SaO2 thấp kèm dấu hiệu suy tim phải).")

    @Rule(OxygenAssessment(PaO2=MATCH.PaO2, SaO2=MATCH.SaO2, polycythemia=True),
          TEST(lambda PaO2, SaO2: 56 <= PaO2 <= 59 or SaO2 <= 88))
    def oxygen_needed_with_polycythemia(self):
        self.declare(Fact(oxygen_required=True))
        print("Bệnh nhân cần thở oxy dài hạn tại nhà (do PaO2 hoặc SaO2 thấp kèm đa hồng cầu).")

    @Rule(OxygenAssessment(PaO2=MATCH.PaO2, SaO2=MATCH.SaO2, pulmonary_hypertension=True),
          TEST(lambda PaO2, SaO2: 56 <= PaO2 <= 59 or SaO2 <= 88))
    def oxygen_needed_with_pulmonary_hypertension(self):
        self.declare(Fact(oxygen_required=True))
        print("Bệnh nhân cần thở oxy dài hạn tại nhà (do PaO2 hoặc SaO2 thấp kèm tăng áp động mạch phổi).")

if __name__ == "__main__":
    # Tạo instance hệ thống
    engine = OxygenTherapyEngine()

    # Khởi tạo hệ thống
    engine.reset()

    # Thu thập dữ liệu từ người dùng
    try:
        PaO2 = float(input("Nhập PaO2 (mmHg): "))
        SaO2 = float(input("Nhập SaO2 (%): "))
        heart_failure = input("Bệnh nhân có dấu hiệu suy tim phải? (True/False): ").strip().lower() == "true"
        polycythemia = input("Bệnh nhân có đa hồng cầu (hematocrit > 55%)? (True/False): ").strip().lower() == "true"
        pulmonary_hypertension = input("Bệnh nhân có tăng áp động mạch phổi? (True/False): ").strip().lower() == "true"

        # Đưa dữ liệu vào hệ thống
        engine.declare(OxygenAssessment(PaO2=PaO2, SaO2=SaO2, heart_failure=heart_failure,
                                        polycythemia=polycythemia, pulmonary_hypertension=pulmonary_hypertension))

        # Chạy hệ thống
        engine.run()

    except ValueError:
        print("Vui lòng nhập dữ liệu hợp lệ.")

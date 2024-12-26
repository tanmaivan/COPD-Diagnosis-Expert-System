from experta import *
from ii_diagnosis_engine import LungFunctionData

class GOLDStageAssessment(KnowledgeEngine):
    @Rule(LungFunctionData(FEV1=MATCH.FEV1))
    def assess_gold_stage(self, FEV1):
        if FEV1 >= 80:
            GOLD_stage = "GOLD 1"
        elif 50 <= FEV1 < 80:
            GOLD_stage = "GOLD 2"
        elif 30 <= FEV1 < 50:
            GOLD_stage = "GOLD 3"
        elif FEV1 < 30:
            GOLD_stage = "GOLD 4"

        self.declare(LungFunctionData(FEV1=FEV1, GOLD_stage=GOLD_stage))

    @Rule(LungFunctionData(GOLD_stage="GOLD 1"))
    def stage_gold_1(self):
        print("Kết quả: Giai đoạn GOLD 1 - Tắc nghẽn nhẹ.")

    @Rule(LungFunctionData(GOLD_stage="GOLD 2"))
    def stage_gold_2(self):
        print("Kết quả: Giai đoạn GOLD 2 - Tắc nghẽn trung bình.")

    @Rule(LungFunctionData(GOLD_stage="GOLD 3"))
    def stage_gold_3(self):
        print("Kết quả: Giai đoạn GOLD 3 - Tắc nghẽn nặng.")

    @Rule(LungFunctionData(GOLD_stage="GOLD 4"))
    def stage_gold_4(self):
        print("Kết quả: Giai đoạn GOLD 4 - Tắc nghẽn rất nặng.")

def run_airway_assessment():
    engine = GOLDStageAssessment()
    engine.reset()
    
    FEV1 = float(input("Nhập giá trị FEV₁ sau test hồi phục phế quản (%): "))

    engine.declare(LungFunctionData(FEV1=FEV1))

    engine.run()

if __name__ == "__main__":
    run_airway_assessment()


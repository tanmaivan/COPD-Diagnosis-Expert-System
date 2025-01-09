from experta import *
from iii_diagnosis_engine import LungFunctionData

class GOLDStageAssessment(KnowledgeEngine):
    @Rule(LungFunctionData(fev1=MATCH.fev1))
    def assess_gold_stage(self, fev1):
        if fev1 >= 80:
            GOLD_stage = "GOLD 1"
            GOLD_stage_description = "Tắc nghẽn nhẹ."
        elif 50 <= fev1 < 80:
            GOLD_stage = "GOLD 2"
            GOLD_stage_description = "Tắc nghẽn trung bình."
        elif 30 <= fev1 < 50:
            GOLD_stage = "GOLD 3"
            GOLD_stage_description = "Tắc nghẽn nặng."
        elif fev1 < 30:
            GOLD_stage = "GOLD 4"
            GOLD_stage_description = "Tắc nghẽn rất nặng."

        self.declare(LungFunctionData(fev1=fev1, GOLD_stage=GOLD_stage, GOLD_stage_description=GOLD_stage_description))

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
    
    fev1 = float(input("Nhập giá trị FEV₁ sau test hồi phục phế quản (%): "))
    engine.declare(LungFunctionData(fev1=fev1))

    engine.run()

if __name__ == "__main__":
    run_airway_assessment()
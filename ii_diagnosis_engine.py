from experta import *

class LungFunctionData(Fact):
    """Fact lưu trữ thông tin kết quả đo chức năng hô hấp"""
    fev1_fvc = Field(float)  # Chỉ số FEV₁/FVC (%)
    copd = Field(bool)  # Chẩn đoán BPTNMT (Có/Không)
    fev1 = Field(float)  # Chỉ số FEV₁ (%)
    GOLD_stage = Field(str)  # Giai đoạn GOLD (GOLD 1/2/3/4)

class DiagnosisEngine(KnowledgeEngine):
    @Rule(LungFunctionData(fev1_fvc=MATCH.fev1_fvc))
    def check_fev1_fvc(self, fev1_fvc):
        if fev1_fvc < 70:
            self.declare(LungFunctionData(fev1_fvc=fev1_fvc, copd=True))
        else:
            self.declare(LungFunctionData(fev1_fvc=fev1_fvc, copd=False))

    @Rule(LungFunctionData(copd=False))
    def normal_diagnosis(self):
        print("Kết quả: Chỉ số FEV₁/FVC bình thường. Không mắc BPTNMT.")
        
    @Rule(LungFunctionData(copd=True))
    def abnormal_diagnosis(self):
        print("Kết quả: Chỉ số FEV₁/FVC dưới 70%. Chẩn đoán: BPTNMT.")

def run_diagnosis_engine():
    engine = DiagnosisEngine()
    
    engine.reset()
    
    while True:
        try:
            fev1_fvc = float(input("Nhập chỉ số FEV₁/FVC (%): "))
            break
        except ValueError:
            print("Vui lòng nhập giá trị số hợp lệ.")

    engine.declare(LungFunctionData(fev1_fvc=fev1_fvc))
        
    engine.run()

    for fact in engine.facts.values():
        if isinstance(fact, Fact) and fact.get("copd") is not None:
            return fact.get("copd")
    return False
        
if __name__ == "__main__":
    run_diagnosis_engine()
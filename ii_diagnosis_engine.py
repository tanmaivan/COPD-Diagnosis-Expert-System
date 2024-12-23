from experta import *

class LungFunctionData(Fact):
    """Fact lưu trữ thông tin kết quả đo chức năng hô hấp"""
    pass

class DiagnosisEngine(KnowledgeEngine):
    @Rule(LungFunctionData(FEV1_FVC=MATCH.FEV1_FVC))
    def check_FEV1_FVC(self, FEV1_FVC):
        if FEV1_FVC < 70:
            self.declare(Fact(FEV1_FVC_status="abnormal"))
        else:
            self.declare(Fact(FEV1_FVC_status="normal"))

    @Rule(Fact(FEV1_FVC_status="normal"))
    def normal_diagnosis(self):
        print("Kết quả: Chỉ số FEV₁/FVC bình thường. Không mắc BPTNMT.")
        
    @Rule(Fact(FEV1_FVC_status="abnormal"))
    def abnormal_diagnosis(self):
        print("Kết quả: Chỉ số FEV₁/FVC dưới 70%. Chẩn đoán: BPTNMT.")

def run_diagnosis_engine():
        # Tạo instance của hệ thống
    engine = DiagnosisEngine()
    
    # Khởi tạo hệ thống
    engine.reset()
    
    while True:
        # Thu thập thông tin từ người dùng
        try:
            FEV1_FVC = float(input("Nhập chỉ số FEV₁/FVC (%): "))
            break
        except ValueError:
            print("Vui lòng nhập giá trị số hợp lệ.")

    # Đưa dữ liệu vào hệ thống
    engine.declare(LungFunctionData(FEV1_FVC=FEV1_FVC))
        
    # Chạy hệ thống
    engine.run()

    for fact in engine.facts.values():
        if isinstance(fact, Fact) and fact.get("FEV1_FVC_status") == "abnormal":
            return True
    return False
        
if __name__ == "__main__":
    run_diagnosis_engine()
from experta import *

class LungFunctionData(Fact):
    """Fact lưu trữ thông tin kết quả đo FEV₁ (%)"""
    pass

class GOLDStageAssessment(KnowledgeEngine):
    @Rule(LungFunctionData(FEV1=MATCH.FEV1))
    def assess_gold_stage(self, FEV1):
        if FEV1 >= 80:
            self.declare(Fact(GOLD_stage="GOLD 1"))
        elif 50 <= FEV1 < 80:
            self.declare(Fact(GOLD_stage="GOLD 2"))
        elif 30 <= FEV1 < 50:
            self.declare(Fact(GOLD_stage="GOLD 3"))
        elif FEV1 < 30:
            self.declare(Fact(GOLD_stage="GOLD 4"))

    @Rule(Fact(GOLD_stage="GOLD 1"))
    def stage_gold_1(self):
        print("Kết quả: Giai đoạn GOLD 1 - Tắc nghẽn nhẹ.")

    @Rule(Fact(GOLD_stage="GOLD 2"))
    def stage_gold_2(self):
        print("Kết quả: Giai đoạn GOLD 2 - Tắc nghẽn trung bình.")

    @Rule(Fact(GOLD_stage="GOLD 3"))
    def stage_gold_3(self):
        print("Kết quả: Giai đoạn GOLD 3 - Tắc nghẽn nặng.")

    @Rule(Fact(GOLD_stage="GOLD 4"))
    def stage_gold_4(self):
        print("Kết quả: Giai đoạn GOLD 4 - Tắc nghẽn rất nặng.")

def run_airway_assessment():
        # Tạo instance của hệ thống
    engine = GOLDStageAssessment()
    
    # Khởi tạo hệ thống
    engine.reset()
    
    # Thu thập thông tin từ người dùng
    try:
        FEV1 = float(input("Nhập giá trị FEV₁ sau test hồi phục phế quản (%): "))
        
        # Đưa dữ liệu vào hệ thống
        engine.declare(LungFunctionData(FEV1=FEV1))
        
        # Chạy hệ thống
        engine.run()
    except ValueError:
        print("Vui lòng nhập giá trị số hợp lệ.")

if __name__ == "__main__":
    run_airway_assessment()

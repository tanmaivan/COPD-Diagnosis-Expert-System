from experta import *

class PatientData(Fact):
    """
    Fact lưu trữ thông tin đánh giá triệu chứng và nguy cơ.
    Các thuộc tính:
    - mMRC: Điểm mMRC (0 - 4).
    - CAT: Điểm CAT (0 - 40).
    - exacerbations: Số đợt cấp trong 12 tháng qua.
    - hospitalizations: Số đợt cấp phải nhập viện trong 12 tháng qua.
    - group: Nhóm ABCD của bệnh nhân
    """
    pass

class SymptomAssessment(KnowledgeEngine):
    @Rule(PatientData(mMRC=MATCH.mMRC, CAT=MATCH.CAT, exacerbations=MATCH.exacerbations, hospitalizations=MATCH.hospitalizations))
    def assess_abcd_group(self, mMRC, CAT, exacerbations, hospitalizations):
        # Phân nhóm nguy cơ đợt cấp
        high_risk = exacerbations >= 2 or hospitalizations >= 1
        low_risk = not high_risk

        # Phân loại triệu chứng
        many_symptoms = mMRC >= 2 or CAT >= 10
        few_symptoms = not many_symptoms

        # Phân nhóm ABCD
        if low_risk and few_symptoms:
            group = "Nhóm A"
        elif low_risk and many_symptoms:
            group = "Nhóm B"
        elif high_risk and few_symptoms:
            group = "Nhóm C"
        elif high_risk and many_symptoms:
            group = "Nhóm D"
        else:
            group = "Không xác định"
        
        self.declare(PatientData(group=group, mMRC=mMRC, CAT=CAT, exacerbations=exacerbations, hospitalizations=hospitalizations))

    @Rule(PatientData(group=MATCH.group))
    def print_group(self, group):
        print(f"Kết quả: Bệnh nhân thuộc {group}.")

# Bộ câu hỏi mMRC
def get_mMRC_score():
    print("\nBảng điểm đánh giá khó thở mMRC:")
    print("0: Khó thở khi gắng sức mạnh.")
    print("1: Khó thở khi đi vội trên đường bằng hoặc đi lên dốc nhẹ.")
    print("2: Đi bộ chậm hơn người cùng tuổi vì khó thở hoặc phải dừng lại để thở.")
    print("3: Phải dừng lại để thở khi đi bộ khoảng 100m trên đường bằng.")
    print("4: Khó thở nhiều đến mức không thể ra khỏi nhà hoặc ngay cả khi thay quần áo.")
    while True:
        try:
            score = int(input("Nhập điểm mMRC (0 - 4): "))
            if 0 <= score <= 4:
                return score
            else:
                print("Vui lòng nhập số trong khoảng từ 0 đến 4.")
        except ValueError:
            print("Vui lòng nhập một số hợp lệ.")

# Bộ câu hỏi CAT
def get_CAT_score():
    print("\nBảng điểm đánh giá CAT (0 - 40):")
    print("Trả lời các câu hỏi với thang điểm từ 0 (tốt) đến 5 (xấu nhất).")
    questions = [
        "1. Tôi hoàn toàn không ho - Tôi ho thường xuyên",
        "2. Tôi không có chút đờm nào trong phổi - Trong phổi tôi có rất nhiều đờm",
        "3. Tôi không có cảm giác nặng ngực - Tôi có cảm giác rất nặng ngực",
        "4. Tôi không bị khó thở khi lên dốc hoặc lên một tầng lầu - Tôi rất khó thở khi lên dốc hoặc lên một tầng lầu",
        "5. Tôi yên tâm ra khỏi nhà dù tôi có bệnh phổi - Tôi không yên tâm chút nào khi ra khỏi nhà vì tôi có bệnh phổi",
        "6. Tôi ngủ ngon giấc - Tôi không ngủ ngon giấc vì tôi có bệnh phổi",
        "7. Tôi cảm thấy rất khỏe - Tôi cảm thấy không còn chút sức lực nào"
    ]
    total_score = 0
    for question in questions:
        while True:
            try:
                print(question)
                score = int(input("Nhập điểm (0 - 5): "))
                if 0 <= score <= 5:
                    total_score += score
                    break
                else:
                    print("Vui lòng nhập số trong khoảng từ 0 đến 5.")
            except ValueError:
                print("Vui lòng nhập một số hợp lệ.")
    return total_score

# Lấy thông tin từ người dùng
def get_patient_data():
    mMRC = get_mMRC_score()
    CAT = get_CAT_score()
    while True:
        try:
            exacerbations = int(input("Nhập số đợt cấp trong 12 tháng qua: "))
            hospitalizations = int(input("Nhập số đợt cấp phải nhập viện trong 12 tháng qua: "))
            return mMRC, CAT, exacerbations, hospitalizations
        except ValueError:
            print("Vui lòng nhập số nguyên hợp lệ.")

class TreatmentPlan(KnowledgeEngine):
    @Rule(PatientData(group=MATCH.group, CAT=MATCH.CAT, mMRC=MATCH.mMRC))
    def treatment_recommendation(self, group, CAT, mMRC):
        print(f"\nBệnh nhân thuộc nhóm {group}.")
        
        # Điều trị chung cho tất cả các nhóm
        self.general_treatment()

        if group == "Nhóm A":
            self.recommend_A()
        elif group == "Nhóm B":
            self.recommend_B(CAT, mMRC)
        elif group == "Nhóm C":
            self.recommend_C()
        elif group == "Nhóm D":
            self.recommend_D(CAT, mMRC)
        else:
            print("Không xác định được nhóm điều trị.")
    
    def general_treatment(self):
        print("Điều trị chung cho tất cả các nhóm:")
        print("- Ngừng tiếp xúc với khói thuốc lá, thuốc lào, bụi, khói bếp rơm, củi, than, khí độc...")
        print("- Cai nghiện thuốc lá, thuốc lào")
        print("- Tiêm vắc xin phòng nhiễm trùng đường hô hấp")
        print("- Vệ sinh tai mũi họng thường xuyên")
        print("- Giữ ấm cổ ngực về mùa lạnh")
        print("- Phát hiện sớm và điều trị kịp thời các nhiễm trùng tai mũi họng, răng hàm mặt\n")

    def recommend_A(self):
        print("Điều trị cho bệnh nhân nhóm A:")
        print("1. Thuốc giãn phế quản khi cần thiết để cải thiện triệu chứng.")
        print("2. Có thể lựa chọn thuốc giãn phế quản tác dụng ngắn hoặc dài.")
        print("3. Tiếp tục điều trị theo phác đồ hoặc thay đổi thuốc tùy vào phản ứng của bệnh nhân.\n")

    def recommend_B(self, CAT, mMRC):
        print("Điều trị cho bệnh nhân nhóm B:")
        if CAT >= 20 or mMRC >= 3:
            print("Khuyến nghị bắt đầu điều trị với phác đồ phối hợp thuốc giãn phế quản LABA/LAMA.")
        else:
            print("Lựa chọn điều trị tối ưu là thuốc giãn phế quản tác dụng dài (LABA hoặc LAMA).")
        print("Lưu ý: Nếu có khó thở dai dẳng, có thể sử dụng phối hợp thuốc giãn phế quản LABA/LAMA.")
        print("Bệnh nhân nhóm B có thể có bệnh đồng mắc, cần đánh giá và điều trị toàn diện.\n")

    def recommend_C(self):
        print("Điều trị cho bệnh nhân nhóm C:")
        print("Khởi đầu điều trị với thuốc giãn phế quản tác dụng dài (LAMA).")
        print("Khuyến nghị sử dụng LAMA để giảm đợt cấp và cải thiện triệu chứng.\n")

    def recommend_D(self, CAT, mMRC):
        print("Điều trị cho bệnh nhân nhóm D:")
        if CAT > 20 or mMRC >= 3:
            print("Khuyến nghị điều trị phối hợp thuốc giãn phế quản LABA/LAMA để giảm triệu chứng và phòng ngừa đợt cấp.")
        else:
            print("Lựa chọn điều trị khởi đầu với thuốc LAMA.")
        print("Nếu bạch cầu ái toan máu ≥ 300 tế bào/µl hoặc bệnh nhân có tiền sử hen, có thể cân nhắc sử dụng ICS/LABA.")
        print("Cần chú ý, ICS có thể làm tăng nguy cơ viêm phổi, chỉ sử dụng khi lợi ích lớn hơn nguy cơ.\n")

def run_symptom_assessment():
    # Tạo instance hệ thống
    engine = SymptomAssessment()
    treatment_engine = TreatmentPlan()
    
    # Khởi tạo hệ thống
    engine.reset()
    treatment_engine.reset()

    # Thu thập dữ liệu bệnh nhân
    mMRC, CAT, exacerbations, hospitalizations = get_patient_data()

    # Đưa dữ liệu vào hệ thống
    engine.declare(PatientData(mMRC=mMRC, CAT=CAT, exacerbations=exacerbations, hospitalizations=hospitalizations))

    # Chạy hệ thống đánh giá triệu chứng
    engine.run()

    # Hỏi người dùng có muốn xem cách điều trị không
    view_treatment = input("Bạn có muốn xem cách điều trị không? (Có/Không): ").strip().lower()
    if view_treatment == "có":
        # Lấy nhóm bệnh nhân từ hệ thống đánh giá triệu chứng
        group_fact = engine.facts[2]  # Giả sử fact thứ 2 là nhóm bệnh nhân
        group = group_fact["group"]

        # Đưa dữ liệu vào hệ thống điều trị
        treatment_engine.declare(PatientData(group=group, mMRC=mMRC, CAT=CAT, exacerbations=exacerbations, hospitalizations=hospitalizations))
        # Chạy hệ thống điều trị
        treatment_engine.run()

if __name__ == "__main__":
    run_symptom_assessment()

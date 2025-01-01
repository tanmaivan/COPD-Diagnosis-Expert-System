from experta import *

class TreatmentData(Fact):
    """
    Fact chứa thông tin về điều trị và triệu chứng của bệnh nhân.
    
    Các thuộc tính:
    - initial_response: Phản ứng ban đầu với điều trị (positive/negative)
    - status: Tình trạng hiện tại: khó thở kéo dài/đợt cấp (persistent/exacerbations)
    - current_treatment: Phác đồ điều trị hiện tại (LABA/LAMA/ICS/LABA/LAMA)
    - second_bronchodilator_effective: Hiệu quả của thuốc giãn phế quản thứ 2
    - eosinophils: Số lượng bạch cầu ái toan
    - fev1: Chỉ số FEV1 (%)
    - chronic_bronchitis: Tình trạng viêm phế quản mạn tính
    - smoker: Tình trạng hút thuốc
    - severe_side_effects: Tác dụng phụ nghiêm trọng
    - treatment_protocol_result: Kết quả phác đồ điều trị
    """
    initial_response = Field(str)
    status = Field(str)
    current_treatment = Field(str)
    second_bronchodilator_effective = Field(bool)
    eosinophils = Field(int)
    fev1 = Field(float)
    chronic_bronchitis = Field(bool)
    smoker = Field(bool)
    severe_side_effects = Field(bool)
    treatment_protocol_result = Field(str)

class TreatmentProtocol(KnowledgeEngine):
    @Rule(TreatmentData(initial_response="positive"))
    def positive_initial_response(self):
        treatment_protocol_result = "Bệnh nhân đáp ứng tốt với phác đồ điều trị ban đầu. Không cần chuyển đổi điều trị thuốc."
        print(treatment_protocol_result)
        self.declare(TreatmentData(treatment_protocol_result=treatment_protocol_result))

    @Rule(TreatmentData(initial_response="negative", status="persistent", current_treatment="LABA"))
    def laba_persistent_status(self):
        treatment_protocol_result = "Bệnh nhân còn khó thở sau điều trị LABA. Khuyến cáo nâng bậc lên LABA/LAMA."
        print(treatment_protocol_result)
        self.declare(TreatmentData(treatment_protocol_result=treatment_protocol_result))

    @Rule(TreatmentData(initial_response="negative", status="persistent", current_treatment="LAMA"))
    def lama_persistent_status(self):
        treatment_protocol_result = "Bệnh nhân còn khó thở sau điều trị LAMA. Khuyến cáo nâng bậc lên LABA/LAMA."
        print(treatment_protocol_result)
        self.declare(TreatmentData(treatment_protocol_result=treatment_protocol_result))

    @Rule(TreatmentData(initial_response="negative", status="persistent", current_treatment="LABA/LAMA", second_bronchodilator_effective=False))
    def laba_lama_no_effect(self):
        treatment_protocol_result = "Thêm thuốc giãn phế quản thứ 2 không cải thiện triệu chứng. Khuyến cáo giảm xuống 1 loại thuốc và xem xét đổi dụng cụ hít hoặc hoạt chất thuốc."
        print(treatment_protocol_result)
        self.declare(TreatmentData(treatment_protocol_result=treatment_protocol_result))

    @Rule(TreatmentData(initial_response="negative", status="persistent", current_treatment="ICS/LABA"))
    def ics_laba_persistent_status(self):
        treatment_protocol_result = "Bệnh nhân khó thở khi điều trị ICS/LABA. Khuyến cáo nâng bậc lên ICS/LABA/LAMA hoặc chuyển sang LABA/LAMA nếu ICS không phù hợp hoặc có tác dụng phụ."
        print(treatment_protocol_result)
        self.declare(TreatmentData(treatment_protocol_result=treatment_protocol_result))

    @Rule(TreatmentData(initial_response="negative", status="exacerbations", current_treatment="LABA"))
    def laba_persistent_exacerbations(self):
        treatment_protocol_result = "Bệnh nhân còn đợt cấp sau điều trị LABA. Khuyến cáo nâng bậc lên LABA/LAMA hoặc ICS/LABA."
        print(treatment_protocol_result)
        self.declare(TreatmentData(treatment_protocol_result=treatment_protocol_result))

    @Rule(TreatmentData(initial_response="negative", status="exacerbations", current_treatment="LAMA"))
    def lama_persistent_exacerbations(self):
        treatment_protocol_result = "Bệnh nhân còn đợt cấp sau điều trị LAMA. Khuyến cáo nâng bậc lên LABA/LAMA hoặc ICS/LABA."
        print(treatment_protocol_result)
        self.declare(TreatmentData(treatment_protocol_result=treatment_protocol_result))

    @Rule(TreatmentData(initial_response="negative", status="exacerbations", current_treatment="LABA/LAMA", eosinophils=P(lambda e: e >= 100)))
    def laba_lama_exacerbations_high_eosinophils(self):
        treatment_protocol_result = "Bệnh nhân còn đợt cấp với bạch cầu ái toan >= 100 tế bào/µL. Khuyến cáo nâng bậc lên ICS/LABA/LAMA."
        print(treatment_protocol_result)
        self.declare(TreatmentData(treatment_protocol_result=treatment_protocol_result))

    @Rule(TreatmentData(initial_response="negative", status="exacerbations", current_treatment="LABA/LAMA", eosinophils=P(lambda e: e < 100)))
    def laba_lama_exacerbations_low_eosinophils(self):
        treatment_protocol_result = "Bệnh nhân còn đợt cấp với bạch cầu ái toan < 100 tế bào/µL. Khuyến cáo thêm Roflumilast hoặc Azithromycin."
        print(treatment_protocol_result)
        self.declare(TreatmentData(treatment_protocol_result=treatment_protocol_result))

    @Rule(TreatmentData(initial_response="negative", exacerbations="persistent", current_treatment="ICS/LABA", eosinophils=P(lambda e: e >= 100)))
    def ics_laba_exacerbations_high_eosinophils(self):
        treatment_protocol_result = "Bệnh nhân còn đợt cấp khi điều trị ICS/LABA. Khuyến cáo nâng bậc lên ICS/LABA/LAMA."
        print(treatment_protocol_result)
        self.declare(TreatmentData(treatment_protocol_result=treatment_protocol_result))

    @Rule(TreatmentData(initial_response="negative", status="exacerbations", current_treatment="ICS/LABA", eosinophils=P(lambda e: e < 100)))
    def ics_laba_exacerbations_low_eosinophils(self):
        treatment_protocol_result = "Bệnh nhân còn đợt cấp khi điều trị ICS/LABA với bạch cầu ái toan < 100 tế bào/µL. Khuyến cáo chuyển sang LABA/LAMA."
        print(treatment_protocol_result)
        self.declare(TreatmentData(treatment_protocol_result=treatment_protocol_result))

    @Rule(TreatmentData(initial_response="negative", status="exacerbations", current_treatment="ICS/LABA/LAMA", fev1=P(lambda f: f < 50), chronic_bronchitis=True))
    def triple_therapy_exacerbations_with_fev1(self):
        treatment_protocol_result = "Bệnh nhân còn đợt cấp khi điều trị ICS/LABA/LAMA. Khuyến cáo thêm Roflumilast cho bệnh nhân có FEV1 < 50% và viêm phế quản mạn tính."
        print(treatment_protocol_result)
        self.declare(TreatmentData(treatment_protocol_result=treatment_protocol_result))

    @Rule(TreatmentData(initial_response="negative", status="exacerbations", current_treatment="ICS/LABA/LAMA", smoker=True))
    def triple_therapy_exacerbations_with_smoking(self):
        treatment_protocol_result = "Bệnh nhân còn đợt cấp khi điều trị ICS/LABA/LAMA. Khuyến cáo thêm Azithromycin cho bệnh nhân từng hút thuốc."
        print(treatment_protocol_result)
        self.declare(TreatmentData(treatment_protocol_result=treatment_protocol_result))

    @Rule(TreatmentData(initial_response="negative", status="exacerbations", current_treatment="ICS/LABA/LAMA", severe_side_effects=True))
    def stop_ics_with_side_effects(self):
        treatment_protocol_result = "Bệnh nhân có tác dụng phụ nghiêm trọng khi điều trị ICS/LABA/LAMA. Khuyến cáo ngừng ICS."
        print(treatment_protocol_result)
        self.declare(TreatmentData(treatment_protocol_result=treatment_protocol_result))

def input_treatment_data():
    """
    Thu thập dữ liệu từ người dùng và tạo một đối tượng TreatmentData.
    """
    print("Hãy trả lời các câu hỏi dưới đây để cung cấp thông tin về tình trạng bệnh nhân:")

    initial_response = input("Phản ứng ban đầu với điều trị (positive/negative): ").strip().lower()
    status = input("Tình trạng hiện tại (persistent/exacerbations): ").strip().lower()
    current_treatment = input("Phác đồ điều trị hiện tại (LABA/LAMA/ICS/LABA/LAMA): ").strip().upper()
    second_bronchodilator_effective = input("Thuốc giãn phế quản thứ 2 có hiệu quả không? (yes/no): ").strip().lower() == "yes"
    eosinophils = int(input("Số lượng bạch cầu ái toan (tế bào/µL): "))
    fev1 = float(input("Chỉ số FEV1 (%): "))
    chronic_bronchitis = input("Bệnh nhân có viêm phế quản mạn tính không? (yes/no): ").strip().lower() == "yes"
    smoker = input("Bệnh nhân có hút thuốc không? (yes/no): ").strip().lower() == "yes"
    severe_side_effects = input("Bệnh nhân có tác dụng phụ nghiêm trọng không? (yes/no): ").strip().lower() == "yes"

    return TreatmentData(
        initial_response=initial_response,
        status=status,
        current_treatment=current_treatment,
        second_bronchodilator_effective=second_bronchodilator_effective,
        eosinophils=eosinophils,
        fev1=fev1,
        chronic_bronchitis=chronic_bronchitis,
        smoker=smoker,
        severe_side_effects=severe_side_effects
    )
if __name__ == "__main__":
    treatment_engine = TreatmentProtocol()
    treatment_engine.reset()
    treatment_data = input_treatment_data()
    treatment_engine.declare(treatment_data)
    treatment_engine.run()

    for fact_id, fact in treatment_engine.facts.items():   
        print(f"Fact ID: {fact_id}")
        for key, value in fact.items():
            print(f"{key}: {value}")

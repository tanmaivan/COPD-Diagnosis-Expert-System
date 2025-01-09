from experta import *
import json

class SymptomAssessmentData(Fact):
    mMRC = Field(int)
    CAT = Field(int)
    exacerbations = Field(int)
    hospitalizations = Field(int)
    group = Field(str)
    general_treatment = Field(list)
    specific_treatment = Field(list)

class SymptomAssessment(KnowledgeEngine):
    @Rule(SymptomAssessmentData(mMRC=MATCH.mMRC, CAT=MATCH.CAT, exacerbations=MATCH.exacerbations, hospitalizations=MATCH.hospitalizations))
    def assess_abcd_group(self, mMRC, CAT, exacerbations, hospitalizations):
        high_risk = exacerbations >= 2 or hospitalizations >= 1
        low_risk = not high_risk

        many_symptoms = mMRC >= 2 or CAT >= 10
        few_symptoms = not many_symptoms

        # Phân nhóm ABCD
        if low_risk and few_symptoms:
            group = "Nhóm A"
        elif low_risk and many_symptoms:
            if CAT >= 20 or mMRC >= 3:
                group = "Nhóm B - Rủi ro cao"
            else:
                group = "Nhóm B"
        elif high_risk and few_symptoms:
            group = "Nhóm C"
        elif high_risk and many_symptoms:
            if CAT >= 20 or mMRC >= 3:
                group = "Nhóm D - Rủi ro cao"
            else:
                group = "Nhóm D"
        else:
            group = "Không xác định"
        
        self.declare(SymptomAssessmentData(group=group, mMRC=mMRC, CAT=CAT, exacerbations=exacerbations, hospitalizations=hospitalizations))

    @Rule(SymptomAssessmentData(group=MATCH.group))
    def print_group(self, group):
        print(f"Kết quả: Bệnh nhân thuộc {group}.")

def load_json(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
    return data

# Bộ câu hỏi mMRC
def get_mMRC_score():
    data = load_json(r"luu_tru_tri_thuc\mmrc_questionnaire.json")
    questions = data["questions"]
    print("\nBảng điểm đánh giá khó thở mMRC:")
    for question in questions:
        print(f"{question['id']}: {question['text']}")
    while True:
        try:
            score = int(input("Nhập điểm mMRC (0 - 4): "))
            if 0 <= score <= 4:
                return score
            else:
                print("Vui lòng nhập số trong khoảng từ 0 đến 4.")
        except ValueError:
            print("Vui lòng nhập một số hợp lệ.")

def get_CAT_score():
    data = load_json(r"luu_tru_tri_thuc\cat_questionnaire.json")
    questions = data["questions"]
    print("\nBảng điểm đánh giá CAT (0 - 40):")
    print("Trả lời các câu hỏi với thang điểm từ 0 (tốt) đến 5 (xấu nhất).")
    total_score = 0
    for question in questions:
        while True:
            try:
                print(f"{question['id']}: {question['text']}")
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
    def __init__(self):
        super().__init__()

        self.treatment_recommendations = load_json(r"luu_tru_tri_thuc\treatment_recommendations.json")
        self.general_treatment = []
        self.specific_treatment = []

    @Rule(SymptomAssessmentData(group=MATCH.group))
    def treatment_recommendation(self, group):     
        if group == "Nhóm A":
            self.recommend_A()
        elif group == "Nhóm B":
            self.recommend_B_high_risk()
        elif group == "Nhóm B - Rủi ro cao":
            self.recommend_B_high_risk()
        elif group == "Nhóm C":
            self.recommend_C()
        elif group == "Nhóm D":
            self.recommend_D()
        elif group == "Nhóm D - Rủi ro cao":
            self.recommend_D_high_risk()
        else:
            print("Không xác định được nhóm điều trị.")

    def recommend_A(self):
        recommendations = self.treatment_recommendations["Nhóm A"]
        print("Điều trị cho bệnh nhân nhóm A:")
        for recommendation in recommendations:
            self.specific_treatment.append(recommendation)
            print(f"- {recommendation}")
        print()
        self.declare(SymptomAssessmentData(specific_treatment=self.specific_treatment))

    def recommend_B(self):
        recommendations = self.treatment_recommendations["Nhóm B"]
        print("Điều trị cho bệnh nhân nhóm B:")
        for recommendation in recommendations["default"]:
            self.specific_treatment.append(recommendation)
            print(f"- {recommendation}")
        print()
        self.declare(SymptomAssessmentData(specific_treatment=self.specific_treatment))

    def recommend_B_high_risk(self):
        recommendations = self.treatment_recommendations["Nhóm B"]
        print("Điều trị cho bệnh nhân nhóm B - Rủi ro cao:")
        for recommendation in recommendations["high_risk"]:
            self.specific_treatment.append(recommendation)
            print(f"- {recommendation}")
        print()
        self.declare(SymptomAssessmentData(specific_treatment=self.specific_treatment))

    def recommend_C(self):
        recommendations = self.treatment_recommendations["Nhóm C"]
        print("Điều trị cho bệnh nhân nhóm C:")
        for recommendation in recommendations:
            self.specific_treatment.append(recommendation)
            print(f"- {recommendation}")
        print()
        self.declare(SymptomAssessmentData(specific_treatment=self.specific_treatment))

    def recommend_D(self):
        recommendations = self.treatment_recommendations["Nhóm D"]
        print("Điều trị cho bệnh nhân nhóm D:")
        for recommendation in recommendations["default"]:
                self.specific_treatment.append(recommendation)
                print(f"- {recommendation}")
        print()
        self.declare(SymptomAssessmentData(specific_treatment=self.specific_treatment))

    def recommend_D_high_risk(self):
        recommendations = self.treatment_recommendations["Nhóm D"]
        print("Điều trị cho bệnh nhân nhóm D - Rủi ro cao:")
        for recommendation in recommendations["high_risk"]:
            self.specific_treatment.append(recommendation)
            print(f"- {recommendation}")
        print()
        self.declare(SymptomAssessmentData(specific_treatment=self.specific_treatment))

def run_symptom_assessment():
    engine = SymptomAssessment()
    treatment_engine = TreatmentPlan()
    
    engine.reset()
    treatment_engine.reset()

    mMRC, CAT, exacerbations, hospitalizations = get_patient_data()

    engine.declare(SymptomAssessmentData(mMRC=mMRC, CAT=CAT, exacerbations=exacerbations, hospitalizations=hospitalizations))

    engine.run()

    view_treatment = input("Bạn có muốn xem cách điều trị ban đầu không? (True/False): ")
    if view_treatment == "True":
        group_fact = engine.facts[2] 
        group = group_fact["group"]

        treatment_recommendations = load_json(r"luu_tru_tri_thuc\treatment_recommendations.json")
        general_treatment = []
        recommendations = treatment_recommendations["general_treatment"]
        for recommendation in recommendations:
            general_treatment.append(recommendation)

        treatment_engine.declare(SymptomAssessmentData(group=group, general_treatment=general_treatment, mMRC=mMRC, CAT=CAT, exacerbations=exacerbations, hospitalizations=hospitalizations))

        treatment_engine.run()
        # for fact_id, fact in treatment_engine.facts.items():   
        #     print(f"Fact ID: {fact_id}")
        #     for key, value in fact.items():
        #         print(f"{key}: {value}")
if __name__ == "__main__":
    run_symptom_assessment()
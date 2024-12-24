import json
from experta import *

class PatientData(Fact):
    """Lưu trữ thông tin của bệnh nhân"""
    pass

class COPDExpertSystem(KnowledgeEngine):
    @Rule(
        AS.f << PatientData(ho=MATCH.ho, khac_dom=MATCH.khac_dom, kho_tho=MATCH.kho_tho, 
                            tuoi_tren_40=MATCH.tuoi_tren_40, hut_thuoc=MATCH.hut_thuoc))
    def screening(self, f, ho, khac_dom, kho_tho, tuoi_tren_40, hut_thuoc):
        # Đếm số câu trả lời "Có"
        symptoms = [ho, khac_dom, kho_tho, tuoi_tren_40, hut_thuoc]
        positive_responses = symptoms.count("Có")
        
        if positive_responses >= 3:
            self.declare(Fact(screening="positive"))
            print("Kết quả: Có nguy cơ BPTNMT. Khuyến cáo đo chức năng hô hấp.")
        else:
            self.declare(Fact(screening="negative"))
            print("Kết quả: Không có nguy cơ BPTNMT.")

    @Rule(Fact(screening="positive"))
    def high_risk_advice(self):
        print("Khuyến cáo đo chức năng hô hấp ngay lập tức để xác định bệnh.")

def load_questions(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data["questions"]

def run_questionnaire_engine():
    questions = load_questions(r"luu_tru_tri_thuc\gold_questionnaire.json")
    engine = COPDExpertSystem()
    engine.reset()

    patient_data = {}
    for question in questions:
        answer = input(f"{question['text']} (Có/Không): ").strip()
        patient_data[question["key"]] = answer

    engine.declare(PatientData(**patient_data))
    engine.run()

    for fact in engine.facts.values():
        if isinstance(fact, Fact) and fact.get("screening") == "positive":
            return True
    return False

if __name__ == "__main__":
    run_questionnaire_engine()
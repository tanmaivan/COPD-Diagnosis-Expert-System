import sys
import os 
from PyQt6.QtWidgets import QMainWindow, QApplication, QLabel, QListWidgetItem, QWidget, QGridLayout, QMessageBox
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QPixmap, QFont
from main_ui import Ui_MainWindow
import json

# Import the engines
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from ii_questionnaire_engine import *
from iii_diagnosis_engine import *
from iv_airway_assessment import *
from v_symptom_assessment import *
from vi_treatment_protocol import *
from vii_long_term_oxygen import *
from viii_lung_intervention_surgery import *
from ix_acute_exacerbation_copd_diagnosis_and_treatment import *
from x_bipap_indication_copd import *
from xi_empirical_antibiotic_selection_outpatient import *
from xii_empirical_antibiotic_selection_inpatient import *

# Define a custom MainWindow class
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Initialize the UI from the generated 'main_ui' class
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Set window properties
        self.setWindowIcon(QIcon("icon\Logo.png"))
        self.setWindowTitle("Hệ chuyên gia Chuẩn đoán bệnh phổi tắc nghẽn mạn tính")

        # Initialize UI elements
        self.title_label = self.ui.title_label
        self.title_label.setText("CS217.P11 - COPD")

        self.title_icon = self.ui.title_icon
        self.title_icon.setText("")
        self.title_icon.setPixmap(QPixmap(r"interface\icon\Logo.png"))
        self.title_icon.setScaledContents(True)

        self.side_menu = self.ui.listWidget
        self.side_menu.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.main_content = self.ui.stackedWidget

        # Define a list of menu items with names and icons
        self.menu_list = [
            {
                "name": "1. Thông tin người khám",
            },
            {
                "name": "2. Sàng lọc phát hiện sớm",
            },
            {
                "name": "3. Đo chức năng hô hấp",
            },
            {
                "name": "4. Độ tắc nghẽn đường thở",
            },
            {
                "name": "5. Chuyển đổi điều trị thuốc",
            },
            {
                "name": "6. Chỉ định thở oxi và nội soi",
            },
            {
                "name": "7. Chẩn đoán đợt cấp",
            },
            {
                "name": "8. Thở máy không xâm nhập",
            },
            {
                "name": "9. Thuốc đợt cấp ngoại trú",
            },
            {
                "name": "10. Thuốc đợt cấp nội trú",
            }
        ]

        # Initialize the UI elements and slots
        self.init_list_widget()
        self.init_stackwidget()
        self.init_single_slot()

        # Connect the button click event to the engines
        self.ui.ii_chan_doan_btn.clicked.connect(self.run_i_questionnaire_engine)
        self.ui.iii_chan_doan_1_btn.clicked.connect(self.run_ii_diagnosis_engine)
        self.ui.iii_chan_doan_2_btn.clicked.connect(self.run_iii_airway_assessment)
        self.ui.v_chan_doan_btn.clicked.connect(self.run_v_symptom_assessment)
        self.ui.vi_kiem_tra_btn.clicked.connect(self.run_vi_treatment_protocol)


    def init_list_widget(self):
        for item in self.menu_list:
            list_item = QListWidgetItem(item["name"])
            self.side_menu.addItem(list_item)

    def change_tab(self, index):
        self.main_content.setCurrentIndex(index)

    def init_single_slot(self):
        self.side_menu.currentRowChanged['int'].connect(self.main_content.setCurrentIndex)

    def init_stackwidget(self):
        # Initialize the stack widget with content pages
        widget_list = self.main_content.findChildren(QWidget)

    def load_json(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
        return data
    
    def run_i_questionnaire_engine(self):
        ho = self.ui.ii_ho.isChecked()
        khac_dom = self.ui.ii_khac_dom.isChecked()
        kho_tho = self.ui.ii_kho_tho.isChecked()
        tuoi_tren_40 = self.ui.ii_tuoi_tren_40.isChecked()
        hut_thuoc = self.ui.ii_hut_thuoc.isChecked()

        engine = COPDExpertSystem()
        engine.reset()
        engine.declare(PatientData(ho=ho, khac_dom=khac_dom, kho_tho=kho_tho, tuoi_tren_40=tuoi_tren_40, hut_thuoc=hut_thuoc))
        engine.run()

        for fact in engine.facts.values():
            if isinstance(fact, Fact) and fact.get("screening") == "positive":
                self.ui.ii_chan_doan.setText("Kết quả: Có nguy cơ bệnh phổi tắc nghẽn mạn tính. Khuyến cáo đo chức năng hô hấp.")
                return
        self.ui.ii_chan_doan.setText("Kết quả: Không có nguy cơ bệnh phổi tắc nghẽn mạn tính.")

    def run_ii_diagnosis_engine(self):
        fev1_fvc = self.ui.iii_fev1_fvc.value()

        engine = DiagnosisEngine()
        engine.reset()
        engine.declare(LungFunctionData(fev1_fvc=fev1_fvc))
        engine.run()

        for fact in engine.facts.values():
            if isinstance(fact, Fact) and fact.get("copd") is not None:
                if not fact.get("copd"):
                    self.ui.iii_ket_qua_1.setText("Kết quả: Chỉ số FEV₁/FVC bình thường. Không mắc BPTNMT.")
                else:
                    self.ui.iii_ket_qua_1.setText("Kết quả: Chỉ số FEV₁/FVC dưới 70%. Chẩn đoán: BPTNMT.")

    def run_iii_airway_assessment(self):
        engine = GOLDStageAssessment()
        engine.reset()

        fev1 = self.ui.iii_fev1.value()

        engine.declare(LungFunctionData(fev1=fev1))
        engine.run()

        for fact in engine.facts.values():
            if isinstance(fact, LungFunctionData) and fact.get("GOLD_stage") is not None:
                self.ui.iii_ket_qua_2.setText(f"Kết quả: Giai đoạn {fact.get('GOLD_stage')} - {fact.get('GOLD_stage_description')}")

    def run_v_symptom_assessment(self):
        engine = SymptomAssessment()
        treatment_engine = TreatmentPlan()
        
        engine.reset()
        treatment_engine.reset()

        mMRC = self.ui.v_mmrc.value()
        CAT = sum([self.ui.v_q1.value(), self.ui.v_q2.value(), self.ui.v_q3.value(), self.ui.v_q4.value(), self.ui.v_q5.value(), self.ui.v_q6.value(), self.ui.v_q7.value(), self.ui.v_q8.value()])
        exacerbations = self.ui.v_exacerbations.value()
        hospitalizations = self.ui.v_hospitalizations.value()

        engine.declare(SymptomAssessmentData(mMRC=mMRC, CAT=CAT, exacerbations=exacerbations, hospitalizations=hospitalizations))

        engine.run()

        for fact in engine.facts.values():
            if isinstance(fact, SymptomAssessmentData):
                group = fact.get("group")

        treatment_recommendations = load_json(r"luu_tru_tri_thuc\treatment_recommendations.json")
        general_treatment = []
        recommendations = treatment_recommendations["general_treatment"]
        for recommendation in recommendations:
            general_treatment.append(recommendation)

        treatment_engine.declare(SymptomAssessmentData(group=group, general_treatment=general_treatment))

        treatment_engine.run()
        facts_list = list(treatment_engine.facts.values())
        general_treatment_list = "\n".join([f"- {item}" for item in facts_list[1].get('general_treatment')])
        specific_treatment_list = "\n".join([f"- {item}" for item in facts_list[2].get('specific_treatment')])

        result_text = (
            f"Kết quả: {group}.\n\n"
            f"Phương pháp điều trị chung:\n {general_treatment_list}.\n\n"
            f"Phương pháp điều trị riêng cho {group}:\n {specific_treatment_list}"
        )
        self.ui.v_ket_qua.setText(result_text)
        msg = QMessageBox()
        msg.setInformativeText(result_text)
        msg.setWindowTitle("Kết quả đánh giá triệu chứng")
        msg.exec()
    
    def run_vi_treatment_protocol(self):
        engine = TreatmentProtocol()
        engine.reset()

        initial_response = self.ui.vi_initial_response.currentText()
        symptoms = self.ui.vi_symptoms.currentText()
        current_treatment = self.ui.vi_current_treatment.currentText()
        second_bronchodilator_effective = self.ui.vi_second_bronchodilator_effective.isChecked()
        eosinophils = self.ui.vi_eosinophils.value()
        fev1 = self.ui.vi_fev1.value()
        chronic_bronchitis = self.ui.vi_chronic_bronchitis.isChecked()
        smoker = self.ui.vi_smoker.isChecked()
        severe_side_effects = self.ui.vi_severe_side_effects.isChecked()

        engine.declare(TreatmentData(initial_response=initial_response, symptoms=symptoms, current_treatment=current_treatment, second_bronchodilator_effective=second_bronchodilator_effective, eosinophils=eosinophils, fev1=fev1, chronic_bronchitis=chronic_bronchitis, smoker=smoker, severe_side_effects=severe_side_effects))

        engine.run()

        for fact in engine.facts.values():
            if isinstance(fact, TreatmentData):
                self.ui.vi_ket_qua.setText(f"Kết quả: {fact.get('treatment_protocol_result')}")


            

if __name__ == '__main__':
    app = QApplication(sys.argv)

    with open("interface\style.qss") as f:
        style_str = f.read()

    app.setStyleSheet(style_str)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
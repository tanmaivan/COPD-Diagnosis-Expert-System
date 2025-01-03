import sys
import os 
from PyQt6.QtWidgets import QMainWindow, QApplication, QLabel, QListWidgetItem, QWidget, QGridLayout, QMessageBox, QPushButton, QTableWidget, QTableWidgetItem
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QPixmap, QFont
from main_ui import Ui_MainWindow

# Import the engines
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from connect_database import ConnectDatabase
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

        # Create a database connection object
        self.db = ConnectDatabase()



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
        self.ui.stackedWidget.setCurrentIndex(0)

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
        self.ui.i_connect.clicked.connect(self.run_i_engine)
        self.ui.ii_chan_doan_btn.clicked.connect(self.run_ii_questionnaire_engine)
        self.ui.iii_chan_doan_1_btn.clicked.connect(self.run_iii_diagnosis_engine)
        self.ui.iii_chan_doan_2_btn.clicked.connect(self.run_iv_airway_assessment)
        self.ui.v_chan_doan_btn.clicked.connect(self.run_v_symptom_assessment)
        self.ui.vi_kiem_tra_btn.clicked.connect(self.run_vi_treatment_protocol)
        self.ui.vii_ket_qua_btn.clicked.connect(self.run_vii_long_term_oxygen)
        self.ui.viii_ket_qua_btn.clicked.connect(self.run_viii_lung_intervention_surgery)
        self.ui.ix_chan_doan_btn.clicked.connect(self.run_ix_acute_exacerbation_copd_diagnosis_and_treatment)
        self.ui.x_ket_qua_btn.clicked.connect(self.run_x_bipap_indication_copd)
        self.ui.xi_ket_qua_btn_1.clicked.connect(self.run_xi_empirical_antibiotic_selection_outpatient_1)
        self.ui.xi_ket_qua_btn_2.clicked.connect(self.run_xi_empirical_antibiotic_selection_outpatient_2)
        self.ui.xi_ket_qua_btn_3.clicked.connect(self.run_xi_empirical_antibiotic_selection_outpatient_3)
        self.ui.xi_ket_qua_btn_4.clicked.connect(self.run_xi_empirical_antibiotic_selection_outpatient_4)
        self.ui.xii_ket_qua_btn_1.clicked.connect(self.run_xii_empirical_antibiotic_selection_inpatient_1)
        self.ui.xii_ket_qua_btn_2.clicked.connect(self.run_xii_empirical_antibiotic_selection_inpatient_2)

        self.ui.xi_ket_qua_btn_2.setEnabled(False)
        self.ui.xi_ket_qua_btn_3.setEnabled(False)
        self.ui.xi_ket_qua_btn_4.setEnabled(False)
        self.ui.xii_ket_qua_btn_2.setEnabled(False)

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
            
    def run_i_engine(self):
        self.ui.i_connect_state.setText("Đã xác nhận.")

        try:
            self.ui.i_add_btn.clicked.disconnect(self.i_add_info)
        except TypeError:
            pass

        self.ui.i_add_btn.clicked.connect(self.i_add_info)
        self.ui.i_update_btn.clicked.connect(self.i_update_info)
        self.ui.i_delete_btn.clicked.connect(self.i_delete_info)
        self.ui.i_select_btn.clicked.connect(self.i_select_info)


        self.result_tb = self.ui.i_result_tb
        self.result_tb.setSortingEnabled(False)

    def i_add_info(self):
        patient_info = self.get_patient_info()

        if not patient_info["full_name"]:
            QMessageBox.warning(self, "Cảnh báo", "Tên đầy đủ là trường bắt buộc.")
            return
        
        add_result = self.db.add_info(**patient_info)
        if add_result:
            QMessageBox.information(self, "Thông báo", f"Thêm thông tin bệnh nhân không thành công.")
        else:
            QMessageBox.information(self, "Thông báo", f"Thêm thông tin bệnh nhân thành công.")
            self.reset_patient_info()
            self.populate_table()
    
    def populate_table(self):
        data = self.db.get_all_info()
        if isinstance(data, Exception):
            QMessageBox.warning(self, "Lỗi", f"Lỗi khi lấy dữ liệu: {data}")
            return

        if data:
            headers = data[0].keys()
            self.result_tb.setColumnCount(len(headers))
            self.result_tb.setHorizontalHeaderLabels(headers)

        self.result_tb.setRowCount(len(data))
        for row_index, row_data in enumerate(data):
            for col_index, (col_name, col_data) in enumerate(row_data.items()):
                self.result_tb.setItem(row_index, col_index, QTableWidgetItem(str(col_data)))

    def reset_patient_info(self):
        self.ui.i_full_name.clear()
        self.ui.i_gender.setCurrentIndex(0)
        self.ui.i_age.setValue(0)
        self.ui.i_address.clear()
        self.ui.i_phone_number.clear()
        self.ui.i_connect_state.clear()
        self.ui.i_connect_state.setText("Vui lòng xác nhận thông tin.")

    def i_update_info(self):
        new_patient = self.get_patient_info()

        if new_patient["full_name"]:
            update_result = self.db.update_info(full_name=new_patient["full_name"], gender=new_patient["gender"], age=new_patient["age"], address=new_patient["address"], phone_number=new_patient["phone_number"])
            if update_result:
                QMessageBox.information(self, "Thông báo", "Cập nhật thông tin bệnh nhân không thành công.")
        else:
            QMessageBox.information(self, "Thông báo", "Vui lòng chọn thông tin bệnh nhân cần cập nhật.")

    def i_delete_info(self):
        select_row = self.result_tb.currentRow()
        if select_row != 1:
            selected_option = QMessageBox.warning(self, "Xác nhận", "Bạn có chắc chắn muốn xóa thông tin bệnh nhân này?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

            if selected_option == QMessageBox.StandardButton.Yes:
                patient_id = self.result_tb.item(select_row, 0).text()
                delete_result = self.db.delete_info(patient_id)
                if delete_result:
                    QMessageBox.information(self, "Thông báo", "Xóa thông tin bệnh nhân không thành công.")
        else:
            QMessageBox.information(self, "Thông báo", "Vui lòng chọn thông tin bệnh nhân cần xóa.")

    def i_select_info(self):
        select_row = self.result_tb.currentRow()
        if select_row != -1:
            full_name = self.result_tb.item(select_row, 1).text()
            gender = self.result_tb.item(select_row, 2).text()
            age = int(self.result_tb.item(select_row, 3).text())
            address = self.result_tb.item(select_row, 4).text()
            phone_number = self.result_tb.item(select_row, 5).text()

            self.full_name.setText(full_name)
            self.gender.setText(gender)
            self.age.setText(str(age))
            self.address.setText(address)
            self.phone_number.setText(phone_number)
        else:
            QMessageBox.information(self, "Thông báo", "Vui lòng chọn thông tin bệnh nhân cần xem.")

    def show_data(self, data):
        if data:
            self.result_tb.setRowCount(0)
            self.result_tb.setRowCount(len(data))

            for row, patient in enumerate(data):
                info_list = [
                    patient["full_name"],
                    patient["gender"],
                    patient["age"],
                    patient["address"],
                    patient["phone_number"]
                ]
                for col, field in enumerate(info_list):
                    cell_item = QTableWidgetItem(str(field))
                    self.result_tb.setItem(row, col, cell_item)

    def get_patient_info(self):
        full_name = self.ui.i_full_name.text()
        gender = self.ui.i_gender.currentText()
        age = self.ui.i_age.value()
        address = self.ui.i_address.text()
        phone_number = self.ui.i_phone_number.text()

        patient_info = {
            "full_name": full_name,
            "gender": gender,
            "age": age,
            "address": address,
            "phone_number": phone_number
        }

        return patient_info




        


    def run_ii_questionnaire_engine(self):
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

    def run_iii_diagnosis_engine(self):
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

    def run_iv_airway_assessment(self):
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
        # msg = QMessageBox()
        # msg.setInformativeText(result_text)
        # msg.setWindowTitle("Kết quả đánh giá triệu chứng")
        # msg.exec()
    
    def run_vi_treatment_protocol(self):
        engine = TreatmentProtocol()
        engine.reset()

        initial_response_text = self.ui.vi_initial_response.currentText()
        initial_response = "positive" if initial_response_text == "Đáp ứng tốt" else "negative"
        status_text = self.ui.vi_status.currentText()
        status = "persistent" if status_text == "Khó thở kéo dài" else "exacerbations"
        current_treatment = self.ui.vi_current_treatment.currentText()
        second_bronchodilator_effective = self.ui.vi_second_bronchodilator_effective.isChecked()
        eosinophils = self.ui.vi_eosinophils.value()
        fev1 = self.ui.vi_fev1.value()
        chronic_bronchitis = self.ui.vi_chronic_bronchitis.isChecked()
        smoker = self.ui.vi_smoker.isChecked()
        severe_side_effects = self.ui.vi_severe_side_effects.isChecked()

        engine.declare(TreatmentData(initial_response=initial_response, status=status, current_treatment=current_treatment, second_bronchodilator_effective=second_bronchodilator_effective, eosinophils=eosinophils, fev1=fev1, chronic_bronchitis=chronic_bronchitis, smoker=smoker, severe_side_effects=severe_side_effects))

        engine.run()

        try:
            result = engine.facts[2].get("treatment_protocol_result")
            self.ui.vi_ket_qua.setText(f"Kết quả: {result}")
        except KeyError:
            self.ui.vi_ket_qua.setText("Không tìm được kết quả.")
    
    def run_vii_long_term_oxygen(self):
        engine = OxygenTherapyEngine()
        engine.reset()

        PaO2 = self.ui.vii_pa02.value()
        SaO2 = self.ui.vii_sa02.value()
        heart_failure = self.ui.vii_heart_failure.isChecked()
        polycythemia = self.ui.vii_polycythemia.isChecked()
        pulmonary_hypertension = self.ui.vii_pulmonary_hypertension.isChecked()

        engine.declare(OxygenAssessment(PaO2=PaO2, SaO2=SaO2, heart_failure=heart_failure, polycythemia=polycythemia, pulmonary_hypertension=pulmonary_hypertension))

        engine.run()

        try:
            oxygen_required = "Chỉ định thở oxy dài hạn.\n" if engine.facts[2].get("oxygen_required") else "Không chỉ định thở oxy.\n"
            long_term_oxygen_reason = "\n".join(engine.facts[2].get("long_term_oxygen_reason"))
            self.ui.vii_ket_qua.setText(f"Kết quả: {oxygen_required}\nLý do:\n{long_term_oxygen_reason}")
        except KeyError:
            self.ui.vii_ket_qua.setText("Không tìm được kết quả.")

    def run_viii_lung_intervention_surgery(self):
        engine = InterventionRecommendation()
        engine.reset()

        emphysema_severity = "nặng" if self.ui.viii_emphysema_severity.currentText() == "Nặng" else "nhẹ"
        lobe_hyperinflation = self.ui.viii_lobe_hyperinflation.isChecked()
        bode_score = self.ui.viii_bode_score.value()
        acute_CO2_exacerbation = self.ui.viii_acute_CO2_exacerbation.isChecked()
        pulmonary_hypertension = self.ui.viii_pulmonary_hypertension.isChecked()
        cor_pulmonale = self.ui.viii_cor_pulmonale.isChecked()
        FEV1 = self.ui.viii_fev1.value()
        DLCO = self.ui.viii_dlco.value()
        emphysema_pattern = "đồng nhất" if self.ui.viii_emphysema_pattern.currentText() == "Đồng nhất" else "không"

        engine.declare(LungInterventionAssessment(emphysema_severity=emphysema_severity, lobe_hyperinflation=lobe_hyperinflation, bode_score=bode_score, acute_CO2_exacerbation=acute_CO2_exacerbation, pulmonary_hypertension=pulmonary_hypertension, cor_pulmonale=cor_pulmonale, FEV1=FEV1, DLCO=DLCO, emphysema_pattern=emphysema_pattern))

        engine.run()

        try:
            diagnosis_result_description = engine.facts[2].get("diagnosis_result_description")
            self.ui.viii_ket_qua.setText(f"Kết quả:\n\n{diagnosis_result_description}")
        except KeyError:
            self.ui.viii_ket_qua.setText("Không tìm được kết quả.")

    def run_ix_acute_exacerbation_copd_diagnosis_and_treatment(self):
        engine = COPDExacerbationDiagnosis()
        engine.reset()

        vas = self.ui.ix_vas.value()
        respiratory_rate = self.ui.ix_respiratory_rate.value()
        heart_rate = self.ui.ix_heart_rate.value()
        spo2 = self.ui.ix_spo2.value()
        crp = self.ui.ix_crp.value()
        pao2 = self.ui.ix_pao2.value()
        paco2 = self.ui.ix_paco2.value()
        ph = self.ui.ix_ph.value()

        engine.declare(COPDExacerbationFacts(vas=vas, respiratory_rate=respiratory_rate, heart_rate=heart_rate, spo2=spo2, crp=crp, pao2=pao2, paco2=paco2, ph=ph))

        engine.run()

        try:
            severity = engine.facts[2].get("severity")
            treatment_location = engine.facts[2].get("treatment_location")
            self.ui.ix_chan_doan.setText(f"Kết quả chẩn đoán: {severity}.\nNên điều trị tại: {treatment_location}.")
        except KeyError:
            self.ui.ix_chan_doan.setText("Không tìm được kết quả.")

    def run_x_bipap_indication_copd(self):
        engine = BiPAPIndicationExpert()
        engine.reset()

        dyspnea_severe = self.ui.x_dyspnea_severe.isChecked()
        ph = self.ui.x_ph.value()
        paco2 = self.ui.x_paco2.value()
        respiratory_rate = self.ui.x_respiratory_rate.value()
        persistent_hypoxemia = self.ui.x_persistent_hypoxemia.isChecked()

        engine.declare(BiPAPIndicationFacts(dyspnea_severe=dyspnea_severe, ph=ph, paco2=paco2, respiratory_rate=respiratory_rate, persistent_hypoxemia=persistent_hypoxemia))

        engine.run()

        try:
            bipap_indicated_description = engine.facts[2].get("bipap_indicated_description")
            self.ui.x_ket_qua.setText(f"Kết quả: {bipap_indicated_description}")
        except KeyError:
            self.ui.x_ket_qua.setText("Không chỉ định thông khí nhân tạo không xâm nhập (BiPAP).") 

    def run_xi_empirical_antibiotic_selection_outpatient_1(self):
        engine_1 = EmpiricalAntibioticSelectionOutpatient()
        engine_1.reset()

        symptom_main_1 = self.ui.xi_breathlessness_increase.isChecked()
        symptom_main_2 = self.ui.xi_sputum_volume_or_thickness_increase.isChecked()
        symptom_main_3 = self.ui.xi_purulent_sputum_increase.isChecked()

        engine_1.declare(Outpatient(breathlessness_increase=symptom_main_1, sputum_volume_or_thickness_increase=symptom_main_2, purulent_sputum_increase=symptom_main_3))
        engine_1.run()

        try:
            antibiotic_selection_description = engine_1.facts[2].get("antibiotic_selection_description")
            if antibiotic_selection_description == "Có đủ triệu chứng chính. Chuyển sang giai đoạn 2.":
                self.ui.xi_ket_qua_btn_2.setEnabled(True)
            else:
                self.ui.xi_ket_qua_btn_2.setEnabled(False)
                self.ui.xi_ket_qua_btn_3.setEnabled(False)
                self.ui.xi_ket_qua_btn_4.setEnabled(False)
                self.ui.xi_ket_qua_2.setText("")
                self.ui.xi_ket_qua_3.setText("")
                self.ui.xi_ket_qua_4.setText("")
            self.ui.xi_ket_qua_1.setText(f"Kết quả chẩn đoán: {antibiotic_selection_description}")
        except KeyError:
            self.ui.ix_chan_doan.setText("Không tìm được kết quả.")

    def run_xi_empirical_antibiotic_selection_outpatient_2(self):
        fev1 = self.ui.xi_fev1.value()
        hospitalization = self.ui.xi_hospitalization.isChecked()
        exacerbations = self.ui.xi_exacerbations.value()
        risk_oxygen_home = self.ui.xi_risk_oxygen_home.isChecked()
        risk_comorbidities = self.ui.xi_risk_comorbidities.isChecked()

        engine_2 = EmpiricalAntibioticSelectionOutpatient()
        engine_2.reset()

        engine_2.declare(Outpatient(fev1=fev1, exacerbations=exacerbations, hospitalization=hospitalization, risk_oxygen_home=risk_oxygen_home, risk_comorbidities=risk_comorbidities))
        engine_2.run()

        try:
            antibiotic_selection_description = engine_2.facts[2].get("antibiotic_selection_description")
            if antibiotic_selection_description == "Có yếu tố nguy cơ kết cục xấu. Chuyển sang giai đoạn 3.":
                self.ui.xi_ket_qua_btn_3.setEnabled(True)
            else:
                self.ui.xi_ket_qua_btn_3.setEnabled(False)
                self.ui.xi_ket_qua_btn_4.setEnabled(False)
                self.ui.xi_ket_qua_3.setText("")
                self.ui.xi_ket_qua_4.setText("")

            self.ui.xi_ket_qua_2.setText(f"Kết quả chẩn đoán: {antibiotic_selection_description}")
        except KeyError:
            self.ui.xi_ket_qua_2.setText("Không tìm được kết quả.")

    def run_xi_empirical_antibiotic_selection_outpatient_3(self):
        engine_3 = EmpiricalAntibioticSelectionOutpatient()
        engine_3.reset()

        risk_pseudomonas = self.ui.xi_risk_pseudomonas.isChecked()

        engine_3.declare(Outpatient(risk_pseudomonas=risk_pseudomonas))
        engine_3.run()

        try:
            antibiotic_selection_description = engine_3.facts[2].get("antibiotic_selection_description")
            if antibiotic_selection_description == "Không có nguy cơ nhiễm Pseudomonas. Chuyển sang giai đoạn 4.":
                self.ui.xi_ket_qua_btn_4.setEnabled(True)
            else:
                self.ui.xi_ket_qua_btn_4.setEnabled(False)
                self.ui.xi_ket_qua_4.setText("")
            self.ui.xi_ket_qua_3.setText(f"Kết quả chẩn đoán: {antibiotic_selection_description}")
        except KeyError:
            self.ui.ix_ix_ket_qua_3.setText("Không tìm được kết quả.")

    def run_xi_empirical_antibiotic_selection_outpatient_4(self):
        engine_4 = EmpiricalAntibioticSelectionOutpatient()
        engine_4.reset()

        fev1 = self.ui.xi_fev1.value()
        bronchiectasis = self.ui.xi_bronchiectasis.isChecked()
        broad_spectrum = self.ui.xi_broad_spectrum_antibiotic_use.isChecked()

        engine_4.declare(Outpatient(fev1=fev1,bronchiectasis=bronchiectasis, broad_spectrum_antibiotic_use=broad_spectrum))
        engine_4.run()

        try:
            antibiotic_selection_description = engine_4.facts[2].get("antibiotic_selection_description")
            self.ui.xi_ket_qua_4.setText(f"Kết quả chẩn đoán: {antibiotic_selection_description}")
        except KeyError:
            self.ui.ix_ix_ket_qua_4.setText("Không tìm được kết quả.")

    def run_xii_empirical_antibiotic_selection_inpatient_1(self):
        engine_1 = EmpiricalAntibioticSelectionInpatient()
        engine_1.reset()

        suspect_pneumonia_or_infection = self.ui.xii_suspect_pneumonia_or_infection.isChecked()

        engine_1.declare(Inpatient(suspect_pneumonia_or_infection=suspect_pneumonia_or_infection))
        engine_1.run()

        try:
            antibiotic_selection_description = engine_1.facts[2].get("antibiotic_selection_description")
            if antibiotic_selection_description == "Không nghi ngờ viêm phổi hoặc nhiễm khuẩn nơi khác. Chuyển sang giai đoạn 2.":
                self.ui.xii_ket_qua_btn_2.setEnabled(True)
            else:  
                self.ui.xii_ket_qua_btn_2.setEnabled(False)
                self.ui.xii_ket_qua_2.setText("")
            self.ui.xii_ket_qua_1.setText(f"Kết quả chẩn đoán: {antibiotic_selection_description}")
        except KeyError:
            self.ui.xii_ket_qua_1.setText("Không tìm được kết quả.")



    def run_xii_empirical_antibiotic_selection_inpatient_2(self):
        engine_2 = EmpiricalAntibioticSelectionInpatient()
        engine_2.reset()

        risk_pseudomonas = self.ui.xii_risk_pseudomonas.isChecked()

        engine_2.declare(Inpatient(risk_pseudomonas=risk_pseudomonas))
        engine_2.run()

        try:
            antibiotic_selection_description_2 = engine_2.facts[2].get("antibiotic_selection_description")
            self.ui.xii_ket_qua_2.setText(f"Kết quả chẩn đoán: {antibiotic_selection_description_2}")
        except KeyError:
            self.ui.xii_ket_qua_2.setText("Không tìm được kết quả.")
        

if __name__ == '__main__':
    app = QApplication(sys.argv)

    with open("interface\style.qss") as f:
        style_str = f.read()

    app.setStyleSheet(style_str)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
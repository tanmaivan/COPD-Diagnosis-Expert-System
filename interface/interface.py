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
                "name": "4. Phân nhóm và điều trị",
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
        self.ui.i_add_btn.clicked.connect(lambda: self.add_database(self.get_patient_info(),"tb_patient_info", "tb_patient_info") if self.get_patient_info() else None)
        self.ui.i_delete_btn.clicked.connect(lambda: self.delete_database("tb_patient_info", "tb_patient_info"))
        self.populate_table("tb_patient_info", "tb_patient_info")

        self.ui.ii_chan_doan_btn.clicked.connect(self.run_ii_questionnaire_engine)
        self.ui.ii_add_btn.clicked.connect(lambda: self.add_database(self.get_ii_questionnaire_data(), "tb_ii_patient_data", "ii_tb") if self.get_ii_questionnaire_data() else None)
        self.ui.ii_delete_btn.clicked.connect(lambda: self.delete_database("tb_ii_patient_data", "ii_tb"))
        self.populate_table("tb_ii_patient_data", "ii_tb")

        self.ui.iii_chan_doan_1_btn.clicked.connect(self.run_iii_diagnosis_engine)
        self.ui.iii_chan_doan_2_btn.clicked.connect(self.run_iv_airway_assessment)
        self.ui.iii_add_btn.clicked.connect(lambda: self.add_database(self.get_iii_lung_function_data(), "tb_iii_lung_function_data", "iii_tb") if self.get_iii_lung_function_data() else None)
        self.ui.iii_delete_btn.clicked.connect(lambda: self.delete_database("tb_iii_lung_function_data", "iii_tb"))
        self.populate_table("tb_iii_lung_function_data", "iii_tb")


        self.ui.v_chan_doan_btn.clicked.connect(self.run_v_symptom_assessment)
        self.ui.v_add_btn.clicked.connect(lambda: self.add_database(self.get_v_symptom_assessment_data(), "tb_v_symptom_assessment_data", "v_tb") if self.get_v_symptom_assessment_data() else None)
        self.ui.v_delete_btn.clicked.connect(lambda: self.delete_database("tb_v_symptom_assessment_data", "v_tb"))
        self.populate_table("tb_v_symptom_assessment_data", "v_tb")

        self.ui.vi_kiem_tra_btn.clicked.connect(self.run_vi_treatment_protocol)
        self.ui.vi_add_btn.clicked.connect(lambda: self.add_database(self.get_vi_treatment_protocol_data(), "tb_vi_treatment_protocol_data", "vi_tb") if self.get_vi_treatment_protocol_data() else None)
        self.ui.vi_delete_btn.clicked.connect(lambda: self.delete_database("tb_vi_treatment_protocol_data", "vi_tb"))
        self.populate_table("tb_vi_treatment_protocol_data", "vi_tb")

        self.ui.vii_ket_qua_btn.clicked.connect(self.run_vii_long_term_oxygen)
        self.ui.vii_add_btn.clicked.connect(lambda: self.add_database(self.get_vii_long_term_oxygen_data(), "tb_vii_long_term_oxygen_data", "vii_tb") if self.get_vii_long_term_oxygen_data() else None)
        self.ui.vii_delete_btn.clicked.connect(lambda: self.delete_database("tb_vii_long_term_oxygen_data", "vii_tb"))
        self.populate_table("tb_vii_long_term_oxygen_data", "vii_tb")

        self.ui.viii_ket_qua_btn.clicked.connect(self.run_viii_lung_intervention_surgery)
        self.ui.viii_add_btn.clicked.connect(lambda: self.add_database(self.get_viii_lung_intervention_surgery_data(), "tb_viii_lung_intervention_surgery_data", "viii_tb") if self.get_viii_lung_intervention_surgery_data() else None)
        self.ui.viii_delete_btn.clicked.connect(lambda: self.delete_database("tb_viii_lung_intervention_surgery_data", "viii_tb"))
        self.populate_table("tb_viii_lung_intervention_surgery_data", "viii_tb")

        self.ui.ix_chan_doan_btn.clicked.connect(self.run_ix_acute_exacerbation_copd_diagnosis_and_treatment)
        self.ui.ix_add_btn.clicked.connect(lambda: self.add_database(self.get_ix_acute_exacerbation_copd_diagnosis_and_treatment_data(), "tb_ix_acute_exacerbation_copd_diagnosis_data", "ix_tb") if self.get_ix_acute_exacerbation_copd_diagnosis_and_treatment_data() else None)
        self.ui.ix_delete_btn.clicked.connect(lambda: self.delete_database("tb_ix_acute_exacerbation_copd_diagnosis_data", "ix_tb"))
        self.populate_table("tb_ix_acute_exacerbation_copd_diagnosis_data", "ix_tb")

        self.ui.x_ket_qua_btn.clicked.connect(self.run_x_bipap_indication_copd)
        self.ui.x_add_btn.clicked.connect(lambda: self.add_database(self.get_x_bipap_indication_copd_data(), "tb_x_bipap_indication_copd_data", "x_tb") if self.get_x_bipap_indication_copd_data() else None)
        self.ui.x_delete_btn.clicked.connect(lambda: self.delete_database("tb_x_bipap_indication_copd_data", "x_tb"))
        self.populate_table("tb_x_bipap_indication_copd_data", "x_tb")

        self.ui.xi_ket_qua_btn_1.clicked.connect(self.run_xi_empirical_antibiotic_selection_outpatient_1)
        self.ui.xi_ket_qua_btn_2.clicked.connect(self.run_xi_empirical_antibiotic_selection_outpatient_2)
        self.ui.xi_ket_qua_btn_3.clicked.connect(self.run_xi_empirical_antibiotic_selection_outpatient_3)
        self.ui.xi_ket_qua_btn_4.clicked.connect(self.run_xi_empirical_antibiotic_selection_outpatient_4)
        self.ui.xi_add_btn.clicked.connect(lambda: self.add_database(self.get_xi_empirical_antibiotic_selection_outpatient_data(), "tb_xi_empirical_antibiotic_selection_outpatient_data", "xi_tb") if self.get_xi_empirical_antibiotic_selection_outpatient_data() else None)
        self.ui.xi_delete_btn.clicked.connect(lambda: self.delete_database("tb_xi_empirical_antibiotic_selection_outpatient_data", "xi_tb"))
        self.populate_table("tb_xi_empirical_antibiotic_selection_outpatient_data", "xi_tb")

        self.ui.xii_ket_qua_btn_1.clicked.connect(self.run_xii_empirical_antibiotic_selection_inpatient_1)
        self.ui.xii_ket_qua_btn_2.clicked.connect(self.run_xii_empirical_antibiotic_selection_inpatient_2)
        self.ui.xii_add_btn.clicked.connect(lambda: self.add_database(self.get_xii_empirical_antibiotic_selection_inpatient_data(), "tb_xii_empirical_antibiotic_selection_inpatient_data", "xii_tb") if self.get_xii_empirical_antibiotic_selection_inpatient_data() else None)
        self.ui.xii_delete_btn.clicked.connect(lambda: self.delete_database("tb_xii_empirical_antibiotic_selection_inpatient_data", "xii_tb"))
        self.populate_table("tb_xii_empirical_antibiotic_selection_inpatient_data", "xii_tb")

        self.ui.iii_chan_doan_2_btn.setEnabled(False)
        self.ui.xi_ket_qua_btn_2.setEnabled(False)
        self.ui.xi_ket_qua_btn_3.setEnabled(False)
        self.ui.xi_ket_qua_btn_4.setEnabled(False)
        self.ui.xii_ket_qua_btn_2.setEnabled(False)

        self.showMaximized()

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

    def populate_table(self, table_name, table_widget_name):
        data = self.db.get_all_info(table_name)
        if isinstance(data, Exception):
            QMessageBox.warning(self, "Lỗi", f"Lỗi khi lấy dữ liệu: {data}")
            return

        table_widget = getattr(self.ui, table_widget_name)
        

        if data:
            headers = list(data[0].keys())
            table_widget.setColumnCount(len(headers))
            table_widget.setHorizontalHeaderLabels(headers)
            table_widget.horizontalHeader().setVisible(True)

            table_widget.setRowCount(len(data))
            for row_index, row_data in enumerate(data):
                for col_index, (col_name, col_data) in enumerate(row_data.items()):
                    table_widget.setItem(row_index, col_index, QTableWidgetItem(str(col_data)))
        else:
            table_widget.setColumnCount(0)
            table_widget.setRowCount(0)
        

    def add_database(self, data, table_name, table_widget_name):   
        add_result = self.db.add_info(table_name, data)
        if add_result:
            QMessageBox.information(self, "Thông báo", f"Thêm thông tin bệnh nhân không thành công.")
        else:
            QMessageBox.information(self, "Thông báo", f"Thêm thông tin bệnh nhân thành công.")
            self.reset_patient_info()
            self.reset_ii_questionnaire()
            self.reset_iii_lung_function_data()
            self.reset_v_symptom_assessment_data()
            self.reset_vi_treatment_protocol_data()
            self.reset_vii_long_term_oxygen_data()
            self.reset_viii_lung_intervention_surgery_data()
            self.reset_ix_acute_exacerbation_copd_diagnosis_and_treatment_data()
            self.reset_x_bipap_indication_copd_data()
            self.reset_xi_empirical_antibiotic_selection_outpatient_data()
            self.reset_xii_empirical_antibiotic_selection_inpatient_data()

            self.populate_table(table_name, table_widget_name)

    def delete_database(self, table_name, table_widget_name):
        primary_key_column = self.db.get_primary_key(table_name)
        if not primary_key_column:
            QMessageBox.warning(self, "Lỗi", "Không tìm thấy khóa chính của bảng.")
            return
        
        table_widget = getattr(self.ui, table_widget_name)

        select_row = table_widget.currentRow()
        if select_row != -1:
            id = int(table_widget.item(select_row, 0).text())
            delete_result = self.db.delete_info(table_name, primary_key_column, id)
            if delete_result:
                QMessageBox.information(self, "Thông báo", f"Xóa thông tin không thành công cho ID: {id}")
            else:
                QMessageBox.information(self, "Thông báo", "Xóa thông tin thành công.")
                self.populate_table(table_name, table_widget_name)
        else:
            QMessageBox.information(self, "Thông báo", "Vui lòng chọn thông tin cần xóa.")

    def get_patient_info(self):
        full_name = self.ui.i_full_name.text()
        gender = self.ui.i_gender.currentText()
        age = self.ui.i_age.value()
        address = self.ui.i_address.text()
        phone_number = self.ui.i_phone_number.text()

        # Kiểm tra các trường bắt buộc
        if not full_name:
            QMessageBox.warning(self, "Lỗi nhập liệu", "Họ và tên không được để trống.")
            return None
        if not gender or gender == "Chọn giới tính":  # Giả sử có mục chọn mặc định
            QMessageBox.warning(self, "Lỗi nhập liệu", "Vui lòng chọn giới tính.")
            return None
        if age <= 0:
            QMessageBox.warning(self, "Lỗi nhập liệu", "Tuổi phải lớn hơn 0.")
            return None
        if not address:
            QMessageBox.warning(self, "Lỗi nhập liệu", "Địa chỉ không được để trống.")
            return None
        if not phone_number:
            QMessageBox.warning(self, "Lỗi nhập liệu", "Số điện thoại không được để trống.")
            return None
        
        patient_info = {
            "full_name": full_name,
            "gender": gender,
            "age": age,
            "address": address,
            "phone_number": phone_number
        }

        return patient_info
    
    def reset_patient_info(self):
        self.ui.i_full_name.clear()
        self.ui.i_gender.setCurrentIndex(0)
        self.ui.i_age.setValue(0)
        self.ui.i_address.clear()
        self.ui.i_phone_number.clear()

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

    def get_ii_questionnaire_data(self):
        patient_id = self.ui.ii_patient_id.value()
        if not self.db.check_patient_exists("tb_patient_info", patient_id):
            QMessageBox.warning(self, "Lỗi", "Mã bệnh nhân không tồn tại trong cơ sở dữ liệu.")
            return None
        
        if self.db.check_patient_exists("tb_ii_patient_data", patient_id):
            QMessageBox.warning(self, "Lỗi", "Dữ liệu bệnh nhân đã tồn tại.")
            return None
        
        ho = self.ui.ii_ho.isChecked()
        khac_dom = self.ui.ii_khac_dom.isChecked()
        kho_tho = self.ui.ii_kho_tho.isChecked()
        tuoi_tren_40 = self.ui.ii_tuoi_tren_40.isChecked()
        hut_thuoc = self.ui.ii_hut_thuoc.isChecked()
        ket_qua = self.ui.ii_chan_doan.toPlainText()


        ii_questionnaire_data = {
            "patient_id": patient_id,
            "ho": ho,
            "khac_dom": khac_dom,
            "kho_tho": kho_tho,
            "tuoi_tren_40": tuoi_tren_40,
            "hut_thuoc": hut_thuoc,
            "ket_qua": ket_qua
        }

        return ii_questionnaire_data
    
    def reset_ii_questionnaire(self):
        self.ui.ii_patient_id.setValue(0)
        self.ui.ii_ho.setChecked(False)
        self.ui.ii_khac_dom.setChecked(False)
        self.ui.ii_kho_tho.setChecked(False)
        self.ui.ii_tuoi_tren_40.setChecked(False)
        self.ui.ii_hut_thuoc.setChecked(False)
        self.ui.ii_chan_doan.setText("")

    def run_iii_diagnosis_engine(self):
        fev1_fvc = self.ui.iii_fev1_fvc.value()

        engine = DiagnosisEngine()
        engine.reset()
        engine.declare(LungFunctionData(fev1_fvc=fev1_fvc))
        engine.run()

        for fact in engine.facts.values():
            if isinstance(fact, Fact) and fact.get("copd") is not None:
                if not fact.get("copd"):
                    self.ui.iii_ket_qua_1.setText("Kết quả: Chỉ số FEV₁/FVC bình thường. Không mắc bệnh phổi tắc nghẽn mạn tính.")
                    self.ui.iii_chan_doan_2_btn.setEnabled(False)
                    self.ui.iii_ket_qua_2.setText("")
                    return fact.get("copd")
                else:
                    self.ui.iii_ket_qua_1.setText("Kết quả: Chỉ số FEV₁/FVC dưới 70%. Chẩn đoán: Mắc bệnh phổi tắc nghẽn mạn tính.")
                    self.ui.iii_chan_doan_2_btn.setEnabled(True)
                    return fact.get("copd")

    def run_iv_airway_assessment(self):

        engine = GOLDStageAssessment()
        engine.reset()

        fev1 = self.ui.iii_fev1.value()

        engine.declare(LungFunctionData(fev1=fev1))
        engine.run()

        for fact in engine.facts.values():
            if isinstance(fact, LungFunctionData) and fact.get("GOLD_stage") is not None:
                self.ui.iii_ket_qua_2.setText(f"Kết quả: Giai đoạn {fact.get('GOLD_stage')} - {fact.get('GOLD_stage_description')}")
                return fact.get("GOLD_stage"), fact.get("GOLD_stage_description")

    def get_iii_lung_function_data(self):
        self.ui.iii_patient_id.value()

        if not self.db.check_patient_exists("tb_patient_info", self.ui.iii_patient_id.value()):
            QMessageBox.warning(self, "Lỗi", "Mã bệnh nhân không tồn tại trong cơ sở dữ liệu.")
            return None
        
        if self.db.check_patient_exists("tb_iii_lung_function_data", self.ui.iii_patient_id.value()):
            QMessageBox.warning(self, "Lỗi", "Dữ liệu bệnh nhân đã tồn tại.")
            return None
        

        fev1_fvc = self.ui.iii_fev1_fvc.value()
        copd = self.run_iii_diagnosis_engine()
        if copd == False:
            gold_stage, gold_stage_description = "", ""
        else:
            gold_stage, gold_stage_description = self.run_iv_airway_assessment()
        fev1 = self.ui.iii_fev1.value()

        iii_lung_function_data = {
            "patient_id": self.ui.iii_patient_id.value(),
            "fev1_fvc": fev1_fvc,
            "copd": copd,
            "fev1": fev1,
            "gold_stage": gold_stage,
            "gold_stage_description": gold_stage_description
        }

        return iii_lung_function_data
    
    def reset_iii_lung_function_data(self):
        self.ui.iii_patient_id.setValue(0)
        self.ui.iii_fev1_fvc.setValue(0)
        self.ui.iii_fev1.setValue(0)
        self.ui.iii_ket_qua_1.setText("")
        self.ui.iii_ket_qua_2.setText("")
        self.ui.iii_chan_doan_2_btn.setEnabled(False)

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

        return group, specific_treatment_list

    def get_v_symptom_assessment_data(self):
        patient_id = self.ui.v_patient_id.value()
        if not self.db.check_patient_exists("tb_patient_info", patient_id):
            QMessageBox.warning(self, "Lỗi", "Mã bệnh nhân không tồn tại trong cơ sở dữ liệu.")
            return None
        
        if self.db.check_patient_exists("tb_v_symptom_assessment_data", patient_id):
            QMessageBox.warning(self, "Lỗi", "Dữ liệu bệnh nhân đã tồn tại.")
            return None

        mMRC = self.ui.v_mmrc.value()
        CAT = sum([self.ui.v_q1.value(), self.ui.v_q2.value(), self.ui.v_q3.value(), self.ui.v_q4.value(), self.ui.v_q5.value(), self.ui.v_q6.value(), self.ui.v_q7.value(), self.ui.v_q8.value()])
        exacerbations = self.ui.v_exacerbations.value()
        hospitalizations = self.ui.v_hospitalizations.value()
        group, specific_treatment = self.run_v_symptom_assessment()

        v_symptom_assessment_data = {
            "patient_id": patient_id,
            "mMRC": mMRC,
            "CAT": CAT,
            "exacerbations": exacerbations,
            "hospitalizations": hospitalizations,
            "grp": group,
            "specific_treatment": json.dumps(specific_treatment)
        }

        return v_symptom_assessment_data
    
    def reset_v_symptom_assessment_data(self):
        self.ui.v_patient_id.setValue(0)
        self.ui.v_mmrc.setValue(0)
        self.ui.v_q1.setValue(0)
        self.ui.v_q2.setValue(0)
        self.ui.v_q3.setValue(0)
        self.ui.v_q4.setValue(0)
        self.ui.v_q5.setValue(0)
        self.ui.v_q6.setValue(0)
        self.ui.v_q7.setValue(0)
        self.ui.v_q8.setValue(0)
        self.ui.v_exacerbations.setValue(0)
        self.ui.v_hospitalizations.setValue(0)
        self.ui.v_ket_qua.setText("")
    
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

    def get_vi_treatment_protocol_data(self):
        patient_id = self.ui.vi_patient_id.value()
        if not self.db.check_patient_exists("tb_patient_info", patient_id):
            QMessageBox.warning(self, "Lỗi", "Mã bệnh nhân không tồn tại trong cơ sở dữ liệu.")
            return None
        
        if self.db.check_patient_exists("tb_vi_treatment_protocol", patient_id):
            QMessageBox.warning(self, "Lỗi", "Dữ liệu bệnh nhân đã tồn tại.")
            return None
        
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
        result = self.ui.vi_ket_qua.toPlainText()

        vi_treatment_protocol_data = {
            "patient_id": patient_id,
            "initial_response": initial_response,
            "status": status,
            "current_treatment": current_treatment,
            "second_bronchodilator_effective": second_bronchodilator_effective,
            "eosinophils": eosinophils,
            "fev1": fev1,
            "chronic_bronchitis": chronic_bronchitis,
            "smoker": smoker,
            "severe_side_effects": severe_side_effects,
            "result": result
        }

        return vi_treatment_protocol_data
    
    def reset_vi_treatment_protocol_data(self):
        self.ui.vi_patient_id.setValue(0)
        self.ui.vi_initial_response.setCurrentIndex(0)
        self.ui.vi_status.setCurrentIndex(0)
        self.ui.vi_current_treatment.setCurrentIndex(0)
        self.ui.vi_second_bronchodilator_effective.setChecked(False)
        self.ui.vi_eosinophils.setValue(0)
        self.ui.vi_fev1.setValue(0)
        self.ui.vi_chronic_bronchitis.setChecked(False)
        self.ui.vi_smoker.setChecked(False)
        self.ui.vi_severe_side_effects.setChecked(False)
        self.ui.vi_ket_qua.setText("")
    
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
            return engine.facts[2].get("oxygen_required"), long_term_oxygen_reason
        except KeyError:
            self.ui.vii_ket_qua.setText("Không tìm được kết quả.")

    def get_vii_long_term_oxygen_data(self):
        patient_id = self.ui.vii_patient_id.value()
        if not self.db.check_patient_exists("tb_patient_info", patient_id):
            QMessageBox.warning(self, "Lỗi", "Mã bệnh nhân không tồn tại trong cơ sở dữ liệu.")
            return None
        
        if self.db.check_patient_exists("tb_vii_long_term_oxygen_data", patient_id):
            QMessageBox.warning(self, "Lỗi", "Dữ liệu bệnh nhân đã tồn tại.")
            return None

        PaO2 = self.ui.vii_pa02.value()
        SaO2 = self.ui.vii_sa02.value()
        heart_failure = self.ui.vii_heart_failure.isChecked()
        polycythemia = self.ui.vii_polycythemia.isChecked()
        pulmonary_hypertension = self.ui.vii_pulmonary_hypertension.isChecked()
        oxygen_required, long_term_oxygen_reason = self.run_vii_long_term_oxygen()

        vii_long_term_oxygen_data = {
            "patient_id": patient_id,
            "PaO2": PaO2,
            "SaO2": SaO2,
            "heart_failure": heart_failure,
            "polycythemia": polycythemia,
            "pulmonary_hypertension": pulmonary_hypertension,
            "oxygen_required": oxygen_required,
            "long_term_oxygen_reason": json.dumps(long_term_oxygen_reason)
        }

        return vii_long_term_oxygen_data
    
    def reset_vii_long_term_oxygen_data(self):
        self.ui.vii_patient_id.setValue(0)
        self.ui.vii_pa02.setValue(0)
        self.ui.vii_sa02.setValue(0)
        self.ui.vii_heart_failure.setChecked(False)
        self.ui.vii_polycythemia.setChecked(False)
        self.ui.vii_pulmonary_hypertension.setChecked(False)
        self.ui.vii_ket_qua.setText("")

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
            diagnosis_result = engine.facts[2].get("diagnosis_result")
            diagnosis_result_description = engine.facts[2].get("diagnosis_result_description")
            self.ui.viii_ket_qua.setText(f"Kết quả:\n\n{diagnosis_result_description}")
            return diagnosis_result, diagnosis_result_description
        except KeyError:
            self.ui.viii_ket_qua.setText("Không tìm được kết quả.")

    def get_viii_lung_intervention_surgery_data(self):
        patient_id = self.ui.viii_patient_id.value()
        if not self.db.check_patient_exists("tb_patient_info", patient_id):
            QMessageBox.warning(self, "Lỗi", "Mã bệnh nhân không tồn tại trong cơ sở dữ liệu.")
            return None
        
        if self.db.check_patient_exists("tb_viii_lung_intervention_surgery_data", patient_id):
            QMessageBox.warning(self, "Lỗi", "Dữ liệu bệnh nhân đã tồn tại.")
            return None

        emphysema_severity = "nặng" if self.ui.viii_emphysema_severity.currentText() == "Nặng" else "nhẹ"
        lobe_hyperinflation = self.ui.viii_lobe_hyperinflation.isChecked()
        bode_score = self.ui.viii_bode_score.value()
        acute_CO2_exacerbation = self.ui.viii_acute_CO2_exacerbation.isChecked()
        pulmonary_hypertension = self.ui.viii_pulmonary_hypertension.isChecked()
        cor_pulmonale = self.ui.viii_cor_pulmonale.isChecked()
        FEV1 = self.ui.viii_fev1.value()
        DLCO = self.ui.viii_dlco.value()
        emphysema_pattern = "đồng nhất" if self.ui.viii_emphysema_pattern.currentText() == "Đồng nhất" else "không"
        diagnosis_result, diagnosis_result_description = self.run_viii_lung_intervention_surgery()

        viii_lung_intervention_surgery_data = {
            "patient_id": patient_id,
            "emphysema_severity": emphysema_severity,
            "lobe_hyperinflation": lobe_hyperinflation,
            "bode_score": bode_score,
            "acute_CO2_exacerbation": acute_CO2_exacerbation,
            "pulmonary_hypertension": pulmonary_hypertension,
            "cor_pulmonale": cor_pulmonale,
            "FEV1": FEV1,
            "DLCO": DLCO,
            "emphysema_pattern": emphysema_pattern,
            "diagnosis_result": diagnosis_result,
            "diagnosis_result_description": json.dumps(diagnosis_result_description)
        }

        return viii_lung_intervention_surgery_data
    
    def reset_viii_lung_intervention_surgery_data(self):
        self.ui.viii_patient_id.setValue(0)
        self.ui.viii_emphysema_severity.setCurrentIndex(0)
        self.ui.viii_lobe_hyperinflation.setChecked(False)
        self.ui.viii_bode_score.setValue(0)
        self.ui.viii_acute_CO2_exacerbation.setChecked(False)
        self.ui.viii_pulmonary_hypertension.setChecked(False)
        self.ui.viii_cor_pulmonale.setChecked(False)
        self.ui.viii_fev1.setValue(0)
        self.ui.viii_dlco.setValue(0)
        self.ui.viii_emphysema_pattern.setCurrentIndex(0)
        self.ui.viii_ket_qua.setText("")  

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
            return severity, treatment_location
        except KeyError:
            self.ui.ix_chan_doan.setText("Không tìm được kết quả.")

    def get_ix_acute_exacerbation_copd_diagnosis_and_treatment_data(self):
        patient_id = self.ui.ix_patient_id.value()
        if not self.db.check_patient_exists("tb_patient_info", patient_id):
            QMessageBox.warning(self, "Lỗi", "Mã bệnh nhân không tồn tại trong cơ sở dữ liệu.")
            return None
        
        if self.db.check_patient_exists("tb_ix_acute_exacerbation_copd_diagnosis_data", patient_id):
            QMessageBox.warning(self, "Lỗi", "Dữ liệu bệnh nhân đã tồn tại.")
            return None

        vas = self.ui.ix_vas.value()
        respiratory_rate = self.ui.ix_respiratory_rate.value()
        heart_rate = self.ui.ix_heart_rate.value()
        spo2 = self.ui.ix_spo2.value()
        crp = self.ui.ix_crp.value()
        pao2 = self.ui.ix_pao2.value()
        paco2 = self.ui.ix_paco2.value()
        ph = self.ui.ix_ph.value()
        diagnosis, treatment_location = self.run_ix_acute_exacerbation_copd_diagnosis_and_treatment()

        ix_acute_exacerbation_copd_diagnosis_and_treatment_data = {
            "patient_id": patient_id,
            "vas": vas,
            "respiratory_rate": respiratory_rate,
            "heart_rate": heart_rate,
            "spo2": spo2,
            "crp": crp,
            "pao2": pao2,
            "paco2": paco2,
            "ph": ph,
            "diagnosis": diagnosis,
            "treatment_location": treatment_location
        }

        return ix_acute_exacerbation_copd_diagnosis_and_treatment_data
    
    def reset_ix_acute_exacerbation_copd_diagnosis_and_treatment_data(self):
        self.ui.ix_patient_id.setValue(0)
        self.ui.ix_vas.setValue(0)
        self.ui.ix_respiratory_rate.setValue(0)
        self.ui.ix_heart_rate.setValue(0)
        self.ui.ix_spo2.setValue(0)
        self.ui.ix_crp.setValue(0)
        self.ui.ix_pao2.setValue(0)
        self.ui.ix_paco2.setValue(0)
        self.ui.ix_ph.setValue(0)
        self.ui.ix_chan_doan.setText("")

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
            return bipap_indicated_description
        except KeyError:
            self.ui.x_ket_qua.setText("Không chỉ định thông khí nhân tạo không xâm nhập (BiPAP).")
            return None
        
    def get_x_bipap_indication_copd_data(self):
        patient_id = self.ui.x_patient_id.value()
        if not self.db.check_patient_exists("tb_patient_info", patient_id):
            QMessageBox.warning(self, "Lỗi", "Mã bệnh nhân không tồn tại trong cơ sở dữ liệu.")
            return None
        
        if self.db.check_patient_exists("tb_x_bipap_indication_copd_data", patient_id):
            QMessageBox.warning(self, "Lỗi", "Dữ liệu bệnh nhân đã tồn tại.")
            return None
        
        dyspnea_severe = self.ui.x_dyspnea_severe.isChecked()
        ph = self.ui.x_ph.value()
        paco2 = self.ui.x_paco2.value()
        respiratory_rate = self.ui.x_respiratory_rate.value()
        persistent_hypoxemia = self.ui.x_persistent_hypoxemia.isChecked()
        bipap_indicated_description = self.run_x_bipap_indication_copd()

        x_bipap_indication_copd_data = {
            "patient_id": patient_id,
            "dyspnea_severe": dyspnea_severe,
            "ph": ph,
            "paco2": paco2,
            "respiratory_rate": respiratory_rate,
            "persistent_hypoxemia": persistent_hypoxemia,
            "bipap_indicated_description": bipap_indicated_description
        }

        return x_bipap_indication_copd_data
    
    def reset_x_bipap_indication_copd_data(self):
        self.ui.x_patient_id.setValue(0)
        self.ui.x_dyspnea_severe.setChecked(False)
        self.ui.x_ph.setValue(0)
        self.ui.x_paco2.setValue(0)
        self.ui.x_respiratory_rate.setValue(0)
        self.ui.x_persistent_hypoxemia.setChecked(False)
        self.ui.x_ket_qua.setText("")

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

    def get_xi_empirical_antibiotic_selection_outpatient_data(self):
        patient_id = self.ui.xi_patient_id.value()
        if not self.db.check_patient_exists("tb_patient_info", patient_id):
            QMessageBox.warning(self, "Lỗi", "Mã bệnh nhân không tồn tại trong cơ sở dữ liệu.")
            return None
        
        if self.db.check_patient_exists("tb_xi_empirical_antibiotic_selection_outpatient_data", patient_id):
            QMessageBox.warning(self, "Lỗi", "Dữ liệu bệnh nhân đã tồn tại.")
            return None
        
        symptom_main_1 = self.ui.xi_breathlessness_increase.isChecked()
        symptom_main_2 = self.ui.xi_sputum_volume_or_thickness_increase.isChecked()
        symptom_main_3 = self.ui.xi_purulent_sputum_increase.isChecked()
        fev1 = self.ui.xi_fev1.value()
        exacerbations = self.ui.xi_exacerbations.value()
        hospitalization = self.ui.xi_hospitalization.isChecked()
        risk_oxygen_home = self.ui.xi_risk_oxygen_home.isChecked()
        risk_comorbidities = self.ui.xi_risk_comorbidities.isChecked()
        risk_pseudomonas = self.ui.xi_risk_pseudomonas.isChecked()
        bronchiectasis = self.ui.xi_bronchiectasis.isChecked()
        broad_spectrum = self.ui.xi_broad_spectrum_antibiotic_use.isChecked()
        antibiotic_selection_description_1 = self.ui.xi_ket_qua_1.toPlainText()
        antibiotic_selection_description_2 = self.ui.xi_ket_qua_2.toPlainText()
        antibiotic_selection_description_3 = self.ui.xi_ket_qua_3.toPlainText()
        antibiotic_selection_description_4 = self.ui.xi_ket_qua_4.toPlainText()

        if antibiotic_selection_description_4:
            antibiotic_selection_description = antibiotic_selection_description_4
        elif antibiotic_selection_description_3:
            antibiotic_selection_description = antibiotic_selection_description_3
        elif antibiotic_selection_description_2:
            antibiotic_selection_description = antibiotic_selection_description_2
        else:
            antibiotic_selection_description = antibiotic_selection_description_1

        xi_empirical_antibiotic_selection_outpatient_data = {
            "patient_id": patient_id,
            "symptom_main_1": symptom_main_1,
            "symptom_main_2": symptom_main_2,
            "symptom_main_3": symptom_main_3,
            "fev1": fev1,
            "exacerbations": exacerbations,
            "hospitalization": hospitalization,
            "risk_oxygen_home": risk_oxygen_home,
            "risk_comorbidities": risk_comorbidities,
            "risk_pseudomonas": risk_pseudomonas,
            "bronchiectasis": bronchiectasis,
            "broad_spectrum": broad_spectrum,
            "antibiotic_selection_description": antibiotic_selection_description
        }

        return xi_empirical_antibiotic_selection_outpatient_data
    
    def reset_xi_empirical_antibiotic_selection_outpatient_data(self):
        self.ui.xi_patient_id.setValue(0)
        self.ui.xi_breathlessness_increase.setChecked(False)
        self.ui.xi_sputum_volume_or_thickness_increase.setChecked(False)
        self.ui.xi_purulent_sputum_increase.setChecked(False)
        self.ui.xi_fev1.setValue(0)
        self.ui.xi_exacerbations.setValue(0)
        self.ui.xi_hospitalization.setChecked(False)
        self.ui.xi_risk_oxygen_home.setChecked(False)
        self.ui.xi_risk_comorbidities.setChecked(False)
        self.ui.xi_risk_pseudomonas.setChecked(False)
        self.ui.xi_bronchiectasis.setChecked(False)
        self.ui.xi_broad_spectrum_antibiotic_use.setChecked(False)
        self.ui.xi_ket_qua_1.setText("")
        self.ui.xi_ket_qua_2.setText("")
        self.ui.xi_ket_qua_3.setText("")
        self.ui.xi_ket_qua_4.setText("")
        self.ui.xi_ket_qua_btn_2.setEnabled(False)
        self.ui.xi_ket_qua_btn_3.setEnabled(False)
        self.ui.xi_ket_qua_btn_4.setEnabled(False)

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

    def get_xii_empirical_antibiotic_selection_inpatient_data(self):
        patient_id = self.ui.xii_patient_id.value()
        if not self.db.check_patient_exists("tb_patient_info", patient_id):
            QMessageBox.warning(self, "Lỗi", "Mã bệnh nhân không tồn tại trong cơ sở dữ liệu.")
            return None
        
        if self.db.check_patient_exists("tb_xii_empirical_antibiotic_selection_inpatient_data", patient_id):
            QMessageBox.warning(self, "Lỗi", "Dữ liệu bệnh nhân đã tồn tại.")
            return None
        
        suspect_pneumonia_or_infection = self.ui.xii_suspect_pneumonia_or_infection.isChecked()
        risk_pseudomonas = self.ui.xii_risk_pseudomonas.isChecked()
        antibiotic_selection_description_1 = self.ui.xii_ket_qua_1.toPlainText()
        antibiotic_selection_description_2 = self.ui.xii_ket_qua_2.toPlainText()

        if antibiotic_selection_description_2:
            antibiotic_selection_description = antibiotic_selection_description_2
        else:
            antibiotic_selection_description = antibiotic_selection_description_1

        xii_empirical_antibiotic_selection_inpatient_data = {
            "patient_id": patient_id,
            "suspect_pneumonia_or_infection": suspect_pneumonia_or_infection,
            "risk_pseudomonas": risk_pseudomonas,
            "antibiotic_selection_description": antibiotic_selection_description
        }

        return xii_empirical_antibiotic_selection_inpatient_data
    
    def reset_xii_empirical_antibiotic_selection_inpatient_data(self):
        self.ui.xii_patient_id.setValue(0)
        self.ui.xii_suspect_pneumonia_or_infection.setChecked(False)
        self.ui.xii_risk_pseudomonas.setChecked(False)
        self.ui.xii_ket_qua_1.setText("")
        self.ui.xii_ket_qua_2.setText("")
        self.ui.xii_ket_qua_btn_2.setEnabled(False)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    with open("interface\style.qss") as f:
        style_str = f.read()

    app.setStyleSheet(style_str)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
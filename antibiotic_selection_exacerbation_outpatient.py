class BPTNMTExpertSystem:
    def __init__(self):
        self.stage = 1

    def check_main_symptoms(self, symptoms):
        """
        Kiểm tra các triệu chứng chính.
        :param symptoms: dict chứa các triệu chứng chính {'kho_tho_tang': bool, 'do_quanh_dom_tang': bool, 'dom_mu_tang': bool}
        """
        main_symptom_count = sum(symptoms.values())
        if main_symptom_count < 2:
            return "Kháng sinh không được chỉ định trừ khi triệu chứng đã xấu hơn dù đã điều trị hỗ trợ phù hợp."
        self.stage = 2
        return "Chuyển đến giai đoạn 2."

    def check_risk_factors(self, risk_factors):
        """
        Kiểm tra các yếu tố nguy cơ cho kết cục xấu.
        :param risk_factors: dict chứa các yếu tố nguy cơ {'FEV1_duoi_50': bool, 'dot_cap_2_lan_12_thang': bool,
                                                           'nhap_vien_dot_cap_3_thang': bool,
                                                           'lieu_phap_oxy_tai_nha': bool,
                                                           'benh_dong_mac': bool}
        """
        if any(risk_factors.values()):
            self.stage = 3
            return "Chuyển đến giai đoạn 3."
        return (
            "Tùy thuộc đặc điểm bệnh nhân, chọn 1 trong các kháng sinh sau:\n"
            "- Macrolide\n"
            "- Cephalosporin thế hệ 2 hoặc 3"
        )

    def check_pseudomonas_risk(self, pseudomonas_risk):
        """
        Kiểm tra nguy cơ nhiễm Pseudomonas.
        :param pseudomonas_risk: bool
        """
        if pseudomonas_risk:
            return "Điều trị bằng ciprofloxacin và cấy đờm làm kháng sinh đồ."
        self.stage = 4
        return "Chuyển đến giai đoạn 4."

    def check_other_pseudomonas_risks(self, other_risks):
        """
        Kiểm tra các yếu tố nguy cơ khác gây nhiễm Pseudomonas.
        :param other_risks: dict chứa các yếu tố nguy cơ {'FEV1_duoi_30': bool, 'gian_phe_quan': bool,
                                                          'khang_sinh_pho_rong_3_thang': bool}
        """
        if any(other_risks.values()):
            return "Điều trị bằng ciprofloxacin hoặc levofloxacin và cấy đờm làm kháng sinh đồ."
        return (
            "Tùy thuộc đặc điểm bệnh nhân, chọn 1 trong các kháng sinh sau:\n"
            "- Amoxicillin-clavulanate\n"
            "- Levofloxacin hoặc moxifloxacin"
        )

# Sử dụng hệ thống chuyên gia
expert_system = BPTNMTExpertSystem()

# Giai đoạn 1: Kiểm tra triệu chứng chính
symptoms = {
    'kho_tho_tang': True,
    'do_quanh_dom_tang': True,
    'dom_mu_tang': False
}
print(expert_system.check_main_symptoms(symptoms))

# Giai đoạn 2: Xét các yếu tố nguy cơ
risk_factors = {
    'FEV1_duoi_50': False,
    'dot_cap_2_lan_12_thang': False,
    'nhap_vien_dot_cap_3_thang': False,
    'lieu_phap_oxy_tai_nha': False,
    'benh_dong_mac': False
}
print(expert_system.check_risk_factors(risk_factors))

# Giai đoạn 3: Kiểm tra nguy cơ nhiễm Pseudomonas
pseudomonas_risk = False
print(expert_system.check_pseudomonas_risk(pseudomonas_risk))

# Giai đoạn 4: Kiểm tra yếu tố nguy cơ khác gây nhiễm Pseudomonas
other_risks = {
    'FEV1_duoi_30': False,
    'gian_phe_quan': False,
    'khang_sinh_pho_rong_3_thang': False
}
print(expert_system.check_other_pseudomonas_risks(other_risks))

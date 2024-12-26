from experta import *

class ThongTinCaNhan(Fact):
    """
    Fact lưu trữ thông tin cá nhân của bệnh nhân.
    Các thuộc tính:
    - ho_ten: Họ tên của bệnh nhân.
    - tuoi: Tuổi của bệnh nhân.
    - dia_chi: Địa chỉ của bệnh nhân.
    - so_dien_thoai: Số điện thoại của bệnh nhân.
    """
    ho_ten: str
    tuoi: int
    dia_chi: str = None
    so_dien_thoai: str

class TrieuChungYTe(Fact):
    """
    Fact lưu trữ các chỉ số y tế của bệnh nhân.
    Các thuộc tính:
    - ho: Bệnh nhân có ho (True/False).
    - khac_dom: Bệnh nhân có khạc đờm (True/False).
    - kho_tho: Bệnh nhân có khó thở (True/False).
    - tuoi_tren_40: Bệnh nhân trên 40 tuổi (True/False).
    - hut_thuoc: Bệnh nhân có hút thuốc (True/False).
    - dot_cap_trong_nam: Số đợt cấp trong năm.
    - nhap_vien_trong_3_thang: Bệnh nhân nhập viện trong 3 tháng qua (True/False).
    - su_dung_oxy_dai_han: Bệnh nhân sử dụng oxy dài hạn (True/False).
    - benh_dong_mac: Bệnh nhân có bệnh đồng mắc (True/False).
    - muc_do_khi_thung: Mức độ khí thũng.
    - gian_no_phoi: Bệnh nhân có giãn nở phổi (True/False).
    - hieu_qua_thuoc_gian_phe_quan_thu_hai: Hiệu quả của thuốc giãn phế quản thứ hai (True/False).
    - dot_cap: Đợt cấp.
    - bach_cau_eosinophil: Số lượng bạch cầu eosinophil.
    - viem_phe_quan_man_tinh: Bệnh nhân có viêm phế quản mạn tính (True/False).
    - hut_thuoc_lau_nam: Bệnh nhân hút thuốc lâu năm (True/False).
    - tac_dung_phu_nghiem_trong: Bệnh nhân có tác dụng phụ nghiêm trọng (True/False).
    - mac_bptnmt: Bệnh nhân mắc BPTNMT (True/False).
    """
    ho: bool = None
    khac_dom: bool = None
    kho_tho: bool = None
    tuoi_tren_40: bool = None
    hut_thuoc: bool = None
    dot_cap_trong_nam: int = None
    nhap_vien_trong_3_thang: bool = None
    su_dung_oxy_dai_han: bool = None
    benh_dong_mac: bool = None
    muc_do_khi_thung: str = None
    gian_no_phoi: bool = None
    hieu_qua_thuoc_gian_phe_quan_thu_hai: bool = None
    dot_cap: str = None
    bach_cau_eosinophil: int = None
    viem_phe_quan_man_tinh: bool = None
    hut_thuoc_lau_nam: bool = None
    tac_dung_phu_nghiem_trong: bool = None
    mac_bptnmt: bool = None

class LungFunctionData(Fact):
    """
    Fact lưu trữ thông tin dữ liệu chức năng phổi là kết quả đo FEV₁ (%).
    Các thuộc tính:
    - FEV1: Chỉ số FEV1 (%).
    - FEV1_FVC: Tỷ lệ FEV1/FVC.
    """
    FEV1: float = None
    FEV1_FVC: float = None

class DuLieuBenhNhan(Fact):
    """
    Fact lưu trữ thông tin của bệnh nhân.
    Các thuộc tính:
    - thong_tin: Thông tin cá nhân của bệnh nhân (Fact ThongTinCaNhan).
    - y_te: Các chỉ số y tế của bệnh nhân (Fact TrieuChungYTe).
    - chuc_nang_phoi: Thông tin kết quả đo FEV₁ (Fact ChucNangPhoi).
    """
    thong_tin: ThongTinCaNhan
    y_te: TrieuChungYTe
    chuc_nang_phoi: ChucNangPhoi

class DanhGiaDotCap(Fact):
    """
    Fact lưu trữ thông tin về đợt cấp BPTNMT.
    Các thuộc tính:
    - muc_do: Mức độ đợt cấp.
    - dieu_tri: Phương pháp điều trị.
    """
    muc_do: str
    dieu_tri: str

class DanhGiaOxy(Fact):
    """
    Fact lưu trữ thông tin đánh giá oxy dài hạn.
    Các thuộc tính:
    - muc_do_oxy: Mức độ oxy.
    - ngay_danh_gia: Ngày đánh giá.
    """
    muc_do_oxy: float
    ngay_danh_gia: str

class PhacDoDieuTri(Fact):
    """
    Fact lưu trữ thông tin về phác đồ điều trị.
    Các thuộc tính:
    - phac_do: Phác đồ điều trị.
    - thuoc: Thuốc điều trị.
    - ngay_tai_kham: Ngày tái khám.
    """
    phac_do: str
    thuoc: str
    ngay_tai_kham: str

class BenhNhanNgoaiTru(Fact):
    """
    Fact lưu trữ thông tin bệnh nhân ngoại trú.
    Các thuộc tính:
    - trieu_chung_chinh_1: Triệu chứng chính 1 (True/False).
    - trieu_chung_chinh_2: Triệu chứng chính 2 (True/False).
    - trieu_chung_chinh_3: Triệu chứng chính 3 (True/False).
    - dot_cap_trong_12_thang: Số đợt cấp trong 12 tháng qua.
    - gian_phe_quan: Bệnh nhân có giãn phế quản (True/False).
    - dung_khang_sinh_pho_rong: Bệnh nhân dùng kháng sinh phổ rộng (True/False).
    - nhap_vien: Bệnh nhân nhập viện (True/False).
    - nguy_co_oxy_tai_nha: Bệnh nhân có nguy cơ cần oxy tại nhà (True/False).
    - benh_dong_mac: Bệnh nhân có bệnh đồng mắc (True/False).
    - nguy_co_pseudomonas: Bệnh nhân có nguy cơ nhiễm Pseudomonas (True/False).
    - pH: Chỉ số pH.
    - paCO2: Chỉ số PaCO2.
    - kho_tho: Bệnh nhân có khó thở (True/False).
    - nhip_tho: Nhịp thở.
    - su_dung_co_ho_hap_phu: Bệnh nhân sử dụng cơ hô hấp phụ (True/False).
    - thay_doi_trang_thai_tam_than: Bệnh nhân có thay đổi trạng thái tâm thần (True/False).
    - nghi_nghiem_viem_phoi_hoac_nhiem_trung: Bệnh nhân nghi ngờ viêm phổi hoặc nhiễm trùng (True/False).
    """
    trieu_chung_chinh_1: bool = False
    trieu_chung_chinh_2: bool = False
    trieu_chung_chinh_3: bool = False
    dot_cap_trong_12_thang: int = None
    gian_phe_quan: bool = False
    dung_khang_sinh_pho_rong: bool = False
    nhap_vien: bool = False
    nguy_co_oxy_tai_nha: bool = False
    benh_dong_mac: bool = False
    nguy_co_pseudomonas: bool = False
    pH: float = None
    paCO2: float = None
    kho_tho: bool = False
    nhip_tho: int = None
    su_dung_co_ho_hap_phu: bool = False
    thay_doi_trang_thai_tam_than: bool = False
    nghi_nghiem_viem_phoi_hoac_nhiem_trung: bool = False

class BenhNhanDieuTri(Fact):
    """
    Fact lưu trữ thông tin về điều trị và triệu chứng của bệnh nhân.
    Các thuộc tính:
    - phan_ung_ban_dau: Phản ứng ban đầu.
    - trieu_chung: Triệu chứng.
    - dieu_tri_hien_tai: Điều trị hiện tại.
    - hieu_qua_thuoc_gian_phe_quan_thu_hai: Hiệu quả của thuốc giãn phế quản thứ hai (True/False).
    - dot_cap: Đợt cấp.
    - bach_cau_eosinophil: Số lượng bạch cầu eosinophil.
    - viem_phe_quan_man_tinh: Bệnh nhân có viêm phế quản mạn tính (True/False).
    - hut_thuoc: Bệnh nhân có hút thuốc (True/False).
    - tac_dung_phu_nghiem_trong: Bệnh nhân có tác dụng phụ nghiêm trọng (True/False).
    """
    phan_ung_ban_dau: str = None
    trieu_chung: str = None
    dieu_tri_hien_tai: str = None
    hieu_qua_thuoc_gian_phe_quan_thu_hai: bool = None
    dot_cap: str = None
    bach_cau_eosinophil: int = None
    viem_phe_quan_man_tinh: bool = None
    hut_thuoc: bool = None
    tac_dung_phu_nghiem_trong: bool = None

class DanhGiaOxy(Fact):
    """
    Fact lưu trữ thông tin về chỉ số oxy và các dấu hiệu liên quan.
    Các thuộc tính:
    - PaO2: Áp lực oxy động mạch (mmHg).
    - SaO2: Độ bão hòa oxy máu (%).
    - suy_tim: Có dấu hiệu suy tim phải (True/False).
    - da_hong_cau: Đa hồng cầu, hematocrit > 55% (True/False).
    - tang_ap_dong_mach_phoi: Tăng áp động mạch phổi (True/False).
    """
    PaO2: float = None
    SaO2: float = None
    suy_tim: bool = False
    da_hong_cau: bool = False
    tang_ap_dong_mach_phoi: bool = False

class DanhGiaBenhNhan(Fact):
    """
    Fact lưu trữ thông tin đánh giá triệu chứng và nguy cơ.
    Các thuộc tính:
    - mMRC: Điểm mMRC (0 - 4).
    - CAT: Điểm CAT (0 - 40).
    - dot_cap: Số đợt cấp trong 12 tháng qua.
    - nhap_vien: Số đợt cấp phải nhập viện trong 12 tháng qua.
    - nhom: Nhóm ABCD của bệnh nhân.
    """
    mMRC: int = None
    CAT: int = None
    dot_cap: int = None
    nhap_vien: int = None
    nhom: str = None

class DanhGiaCanThiep(Fact):
    """
    Fact lưu trữ thông tin đánh giá chỉ định nội soi can thiệp hoặc phẫu thuật.
    Các thuộc tính:
    - muc_do_khi_phe_thung: Mức độ khí phế thũng (nặng hoặc nhẹ).
    - u_khi_thuy_tren: Ứ khí thùy trên (True/False).
    - diem_BODE: Điểm BODE (0 - 10).
    - dot_cap_tang_CO2: Có đợt cấp với tăng CO2 máu cấp tính (True/False).
    - tang_ap_dong_mach_phoi: Có tăng áp động mạch phổi (True/False).
    - tam_phe_man: Có tâm phế mạn (True/False).
    - DLCO: Chỉ số DLCO (%).
    - kieu_hinh_khi_phe_thung: Kiểu hình khí phế thũng (đồng nhất hoặc không).
    """
    muc_do_khi_phe_thung: str = None
    u_khi_thuy_tren: bool = False
    diem_BODE: int = None
    dot_cap_tang_CO2: bool = False
    tang_ap_dong_mach_phoi: bool = False
    tam_phe_man: bool = False
    DLCO: float = None
    kieu_hinh_khi_phe_thung: str = None
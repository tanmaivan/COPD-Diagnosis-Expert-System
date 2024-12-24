from experta import Fact

class ThongTinCaNhan(Fact):
    """Lưu trữ thông tin cá nhân của bệnh nhân"""
    ho_ten: str
    tuoi: int
    dia_chi: str
    so_dien_thoai: str

class DuLieuYTe(Fact):
    """Lưu trữ các chỉ số y tế của bệnh nhân"""
    ho: bool = None
    khac_dom: bool = None
    kho_tho: bool = None
    tuoi_tren_40: bool = None
    hut_thuoc: bool = None
    fev1: float = None
    fev1_fvc: float = None
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
    mac_bptnmt: bool = None  # Thêm biến này

class DanhGiaDotCap(Fact):
    """Fact lưu trữ thông tin về đợt cấp BPTNMT"""
    muc_do: str
    dieu_tri: str

class DanhGiaOxy(Fact):
    """Fact lưu trữ thông tin đánh giá oxy dài hạn"""
    muc_do_oxy: float
    ngay_danh_gia: str

class DuLieuDieuTri(Fact):
    """Fact lưu trữ thông tin về phác đồ điều trị"""
    phac_do: str
    thuoc: str
    ngay_tai_kham: str
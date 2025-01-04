<!-- Banner -->
<p align="center">
  <a href="https://www.uit.edu.vn/" title="Trường Đại học Công nghệ Thông tin" style="border: none;">
    <img src="https://i.imgur.com/WmMnSRt.png" alt="Trường Đại học Công nghệ Thông tin | University of Information Technology">
  </a>
</p>

<h1 align="center"><b>CÁC HỆ CƠ SỞ TRI THỨC</b></h1>

# Thành viên nhóm
| STT    | MSSV          | Họ và Tên              |Chức Vụ    | Email                   |
| ------ |:-------------:| ----------------------:|----------:|-------------------------:
| 1      | 22521301      | Mai Văn Tân            |Nhóm trưởng|22521301@gm.uit.edu.vn   |
| 2      | 22521568      | Trần Lê Nguyên Trung   |Thành viên |22521568@gm.uit.edu.vn   |
| 3      | 22521550      | Nguyễn Công Trúc       |Thành viên |22521550@gm.uit.edu.vn   |
| 4      | 22521391      | Nguyễn Minh Thiện      |Thành viên |22521692@gm.uit.edu.vn   |

# GIỚI THIỆU MÔN HỌC
* **Tên môn học:** Hệ cơ sở tri thức
* **Mã môn học:** CS217
* **Mã lớp:** CS217.P11
* **Năm học:** HK1 (2024 - 2025)
* **GV Lý Thuyết:** Nguyễn Thị Ngọc Diễm
* **GV HDTH:** Nguyễn Thị Ngọc Diễm

# ĐỒ ÁN CUỐI KÌ
* **Đề tài:** Xây dựng hệ chuyên gia chẩn đoán và điều trị bệnh phổi tắc nghẽn mạn tính

# MÔ TẢ SƠ LƯỢC:
- Nhằm xây dựng phần mềm chuẩn đoán tình trạng của người dùng và đưa ra các chuẩn đoán bệnh và điều trị tương ứng qua việc người dừng tham gia trả lời các bộ câu hỏi chuẩn đoán.

# CÔNG NGHỆ SỬ DỤNG
- Phần mềm Chuyên gia chuẩn đoán sử dụng các công nghệ liệt kê dưới đây:
  + [Experta](https://github.com/nilp0inter/experta) sử dụng để xây dựng bộ suy diễn.
  + [PyQt6](https://pypi.org/project/PyQt6/) sử dụng để xây dựng giao diện người dùng.
  + ___ sử dụng để làm cơ sở dữ liệu lưu trữ thông tin.

# MÔI TRƯỜNG CÀI ĐẶT VÀ SỬ DỤNG PHẦN MỀM
- Cài đặt môi trường cần thiết:
```md
pip install experta PyQt6
```
- Chạy chương trình bằng các thực thi câu lệnh sau trong tệp tin của chương trình:
```md
python /interface/interface.py
```

Hướng dẫn kết nối CSDL
1. Cài đặt MySQL Workbench và MySQL Server Community
Tải và cài đặt MySQL Server Community từ trang chủ MySQL: MySQL Server Community Edition.
Tải và cài đặt MySQL Workbench từ trang chủ MySQL: MySQL Workbench.
2. Tạo cơ sở dữ liệu từ file schema.sql
Mở MySQL Workbench:
Kết nối đến server MySQL mà bạn đã cài đặt.
Tạo cơ sở dữ liệu:
Trong MySQL Workbench, mở file schema.sql bằng cách:
Vào menu File → Open SQL Script, sau đó chọn file schema.sql.
Nhấn vào biểu tượng Lightning Bolt hoặc nhấn Ctrl + Enter để chạy file script.
Xác nhận tạo bảng:
Kiểm tra trong mục Schemas để chắc chắn rằng các bảng đã được tạo đúng theo định nghĩa trong file schema.sql.
3. Cấu hình kết nối ứng dụng
Đảm bảo ứng dụng được cấu hình đúng để kết nối tới cơ sở dữ liệu MySQL.
Kiểm tra file cấu hình của ứng dụng (nếu có), hoặc đảm bảo rằng các thông tin sau được khai báo đúng:
Host: localhost (hoặc địa chỉ máy chủ khác nếu server không cài đặt trên máy local)
Port: 3306 (mặc định của MySQL)
User: Tên người dùng MySQL của bạn (thường là root)
Password: Mật khẩu bạn đã đặt khi cài MySQL.
Sử dụng ứng dụng
Sau khi hoàn tất các bước trên, bạn có thể chạy ứng dụng để sử dụng đầy đủ các chức năng của hệ chuyên gia.
Nếu gặp lỗi kết nối, vui lòng kiểm tra lại thông tin kết nối trong ứng dụng.

<!-- Footer
<p align='center'>Copyright lololol</p> -->

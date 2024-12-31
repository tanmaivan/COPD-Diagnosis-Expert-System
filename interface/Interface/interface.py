import sys
from PyQt6.QtWidgets import QMainWindow, QApplication, QLabel, QListWidgetItem, QWidget, QGridLayout
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QPixmap, QFont

# Import the UI class from the 'main_ui' module
from main_ui import Ui_MainWindow


# Define a custom MainWindow class
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Initialize the UI from the generated 'main_ui' class
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Set window properties
        self.setWindowIcon(QIcon("interface\Interface\icon\Logo.png"))
        self.setWindowTitle("Hệ chuyên gia Chuẩn đoán bệnh phổi tắc nghẽn mạn tính")

        # Initialize UI elements
        self.title_label = self.ui.title_label
        self.title_label.setText("CS217.P11 - COPD")

        self.title_icon = self.ui.title_icon
        self.title_icon.setText("")
        self.title_icon.setPixmap(QPixmap("interface\Interface\icon\Logo.png"))
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
                "name": "3. Chẩn đoán xác định",
            },
            {
                "name": "4. Độ tắc nghẽn đường thở",
            },
            {
                "name": "5. Cách điều trị",
            },
            {
                "name": "6. Chuyển đổi điều trị thuốc",
            },
            {
                "name": "7. Chỉ định thở oxi",
            },
            {
                "name": "8. Chỉ định nội soi",
            },
            {
                "name": "9. Chẩn đoán đợt cấp",
            },
            {
                "name": "10. Thở máy không xâm nhập",
            },
            {
                "name": "11. Thuốc đợt cấp ngoại trú",
            },
            {
                "name": "12. Thuốc đợt cấp nội trú",
            }
        ]

        # Initialize the UI elements and slots
        self.init_list_widget()
        self.init_stackwidget()
        self.init_single_slot()

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

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Load style file
    with open("interface\Interface\style.qss") as f:
        style_str = f.read()

    app.setStyleSheet(style_str)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())

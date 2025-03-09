from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QFileDialog
from src.database.db import get_connection
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from src.database.db import get_db
from src.models.company import Company
from sqlalchemy.orm import Session

class CompanyManagement(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        # Main layout
        main_layout = QVBoxLayout()
        
        # Form layout
        form_layout = QHBoxLayout()
        
        # Company Name
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Company Name")
        form_layout.addWidget(self.name_input)
        
        # Logo Upload
        self.logo_label = QLabel("No Logo Selected")
        self.logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.logo_label.setFixedSize(100, 100)
        self.logo_label.setStyleSheet("border: 1px solid #ccc;")
        
        self.logo_button = QPushButton("Upload Logo")
        self.logo_button.clicked.connect(self.upload_logo)
        
        logo_layout = QVBoxLayout()
        logo_layout.addWidget(self.logo_label)
        logo_layout.addWidget(self.logo_button)
        form_layout.addLayout(logo_layout)
        
        # Add Company Button
        self.add_button = QPushButton("Add Company")
        self.add_button.clicked.connect(self.add_company)
        form_layout.addWidget(self.add_button)
        
        main_layout.addLayout(form_layout)
        
        # Companies Table
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["ID", "Name", "Logo"])
        self.table.setColumnWidth(0, 50)
        self.table.setColumnWidth(1, 300)
        self.table.setColumnWidth(2, 100)
        main_layout.addWidget(self.table)
        
        self.setLayout(main_layout)
        self.load_companies()
        
    def upload_logo(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Select Logo", "", "Images (*.png *.jpg *.jpeg)"
        )
        if file_name:
            pixmap = QPixmap(file_name)
            self.logo_label.setPixmap(pixmap.scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio))
            self.logo_path = file_name
            
    def add_company(self):
        name = self.name_input.text()
        if not name:
            return
            
        with Session(get_db()) as db:
            company = Company(name=name, logo_path=self.logo_path)
            db.add(company)
            db.commit()
            
        self.load_companies()
        self.name_input.clear()
        self.logo_label.clear()
        self.logo_label.setText("No Logo Selected")
        
    def load_companies(self):
        from sqlalchemy import select
        with get_connection() as conn:
            companies = conn.execute(select(Company)).all()
            self.table.setRowCount(len(companies))
            for row, company in enumerate(companies):
                self.table.setItem(row, 0, QTableWidgetItem(str(company.id)))
                self.table.setItem(row, 1, QTableWidgetItem(company.name))
                if company.logo_path:
                    pixmap = QPixmap(company.logo_path)
                    label = QLabel()
                    label.setPixmap(pixmap.scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio))
                    self.table.setCellWidget(row, 2, label)

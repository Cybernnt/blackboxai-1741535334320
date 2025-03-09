from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QFileDialog, QComboBox, QDateEdit, QDoubleSpinBox
from src.database.db import get_connection
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QPixmap
from src.database.db import get_db
from src.models.product import Product
from src.models.company import Company
from src.models.category import Category
from sqlalchemy.orm import Session

class ProductManagement(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        # Main layout
        main_layout = QVBoxLayout()
        
        # Form layout
        form_layout = QHBoxLayout()
        
        # Product Name
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Product Name")
        form_layout.addWidget(self.name_input)
        
        # Company Selection
        self.company_combo = QComboBox()
        self.company_combo.addItem("Select Company")
        form_layout.addWidget(self.company_combo)
        
        # Category Selection
        self.category_combo = QComboBox()
        self.category_combo.addItem("Select Category")
        form_layout.addWidget(self.category_combo)
        
        # Image Upload
        self.image_label = QLabel("No Image Selected")
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setFixedSize(100, 100)
        self.image_label.setStyleSheet("border: 1px solid #ccc;")
        
        self.image_button = QPushButton("Upload Image")
        self.image_button.clicked.connect(self.upload_image)
        
        image_layout = QVBoxLayout()
        image_layout.addWidget(self.image_label)
        image_layout.addWidget(self.image_button)
        form_layout.addLayout(image_layout)
        
        # Add Product Button
        self.add_button = QPushButton("Add Product")
        self.add_button.clicked.connect(self.add_product)
        form_layout.addWidget(self.add_button)
        
        main_layout.addLayout(form_layout)
        
        # Details Form
        details_layout = QHBoxLayout()
        
        # HSN Code
        self.hsn_input = QLineEdit()
        self.hsn_input.setPlaceholderText("HSN Code")
        details_layout.addWidget(self.hsn_input)
        
        # Flavor
        self.flavor_input = QLineEdit()
        self.flavor_input.setPlaceholderText("Flavor")
        details_layout.addWidget(self.flavor_input)
        
        # Weight
        self.weight_input = QDoubleSpinBox()
        self.weight_input.setSuffix(" g")
        self.weight_input.setRange(0, 10000)
        self.weight_input.setValue(0)
        details_layout.addWidget(self.weight_input)
        
        # MRP
        self.mrp_input = QDoubleSpinBox()
        self.mrp_input.setPrefix("₹ ")
        self.mrp_input.setRange(0, 10000)
        self.mrp_input.setValue(0)
        details_layout.addWidget(self.mrp_input)
        
        # Purchase Cost
        self.purchase_input = QDoubleSpinBox()
        self.purchase_input.setPrefix="₹ "
        self.purchase_input.setRange(0, 10000)
        self.purchase_input.setValue(0)
        details_layout.addWidget(self.purchase_input)
        
        # Selling Cost
        self.selling_input = QDoubleSpinBox()
        self.selling_input.setPrefix="₹ "
        self.selling_input.setRange(0, 10000)
        self.selling_input.setValue(0)
        details_layout.addWidget(self.selling_input)
        
        # Expiry Date
        self.expiry_input = QDateEdit()
        self.expiry_input.setDate(QDate.currentDate())
        self.expiry_input.setCalendarPopup(True)
        details_layout.addWidget(self.expiry_input)
        
        # Stock Quantity
        self.stock_input = QDoubleSpinBox()
        self.stock_input.setRange(0, 10000)
        self.stock_input.setValue=0
        details_layout.addWidget(self.stock_input)
        
        main_layout.addLayout(details_layout)
        
        # Products Table
        self.table = QTableWidget()
        self.table.setColumnCount(10)
        self.table.setHorizontalHeaderLabels([
            "ID", "Name", "Company", "Category", "HSN", "Flavor", 
            "Weight", "MRP", "Stock", "Expiry"
        ])
        self.table.setColumnWidth(0, 50)
        self.table.setColumnWidth(1, 200)
        self.table.setColumnWidth(2, 150)
        self.table.setColumnWidth(3, 150)
        self.table.setColumnWidth(4, 100)
        self.table.setColumnWidth(5, 100)
        self.table.setColumnWidth(6, 80)
        self.table.setColumnWidth(7, 80)
        self.table.setColumnWidth(8, 80)
        self.table.setColumnWidth(9, 100)
        main_layout.addWidget(self.table)
        
        self.setLayout(main_layout)
        self.load_companies()
        self.load_products()
        
    def upload_image(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Select Product Image", "", "Images (*.png *.jpg *.jpeg)"
        )
        if file_name:
            pixmap = QPixmap(file_name)
            self.image_label.setPixmap(pixmap.scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio))
            self.image_path = file_name
            
    def add_product(self):
        name = self.name_input.text()
        company_id = self.company_combo.currentData()
        category_id = self.category_combo.currentData()
        hsn_code = self.hsn_input.text()
        flavor = self.flavor_input.text()
        weight = self.weight_input.value()
        mrp = self.mrp_input.value()
        purchase_cost = self.purchase_input.value()
        selling_cost = self.selling_input.value()
        expiry_date = self.expiry_input.date().toPyDate()
        stock_quantity = self.stock_input.value()
        
        if not all([name, company_id, category_id]):
            return
            
        with Session(get_db()) as db:
            product = Product(
                name=name,
                company_id=company_id,
                category_id=category_id,
                hsn_code=hsn_code,
                flavor=flavor,
                weight=weight,
                mrp=mrp,
                purchase_cost=purchase_cost,
                selling_cost=selling_cost,
                expiry_date=expiry_date,
                stock_quantity=stock_quantity,
                image_path=self.image_path
            )
            db.add(product)
            db.commit()
            
        self.load_products()
        self.clear_form()
        
    def load_companies(self):
        from sqlalchemy import select
        with get_connection() as conn:
            companies = conn.execute(select(Company)).all()
            self.company_combo.clear()
            self.company_combo.addItem("Select Company")
            for company in companies:
                self.company_combo.addItem(company.name, company.id)
                
    def load_products(self):
        from sqlalchemy import select
        with get_connection() as conn:
            products = conn.execute(select(Product)).all()
            self.table.setRowCount(len(products))
            for row, product in enumerate(products):
                self.table.setItem(row, 0, QTableWidgetItem(str(product.id)))
                self.table.setItem(row, 1, QTableWidgetItem(product.name))
                self.table.setItem(row, 2, QTableWidgetItem(product.company.name))
                self.table.setItem(row, 3, QTableWidgetItem(product.category.name))
                self.table.setItem(row, 4, QTableWidgetItem(product.hsn_code))
                self.table.setItem(row, 5, QTableWidgetItem(product.flavor))
                self.table.setItem(row, 6, QTableWidgetItem(f"{product.weight} g"))
                self.table.setItem(row, 7, QTableWidgetItem(f"₹{product.mrp}"))
                self.table.setItem(row, 8, QTableWidgetItem(str(product.stock_quantity)))
                self.table.setItem(row, 9, QTableWidgetItem(product.expiry_date.strftime("%Y-%m-%d")))
                
    def clear_form(self):
        self.name_input.clear()
        self.company_combo.setCurrentIndex(0)
        self.category_combo.setCurrentIndex(0)
        self.hsn_input.clear()
        self.flavor_input.clear()
        self.weight_input.setValue(0)
        self.mrp_input.setValue(0)
        self.purchase_input.setValue(0)
        self.selling_input.setValue=0
        self.expiry_input.setDate(QDate.currentDate())
        self.stock_input.setValue=0
        self.image_label.clear()
        self.image_label.setText("No Image Selected")

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QComboBox, QDoubleSpinBox
from src.database.db import get_connection
from PyQt6.QtCore import Qt
from src.database.db import get_db
from src.models.sales import Sale
from src.models.product import Product
from sqlalchemy.orm import Session

class SalesManagement(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        # Main layout
        main_layout = QVBoxLayout()
        
        # Form layout
        form_layout = QHBoxLayout()
        
        # Product Selection
        self.product_combo = QComboBox()
        self.product_combo.addItem("Select Product")
        form_layout.addWidget(self.product_combo)
        
        # Quantity
        self.quantity_input = QDoubleSpinBox()
        self.quantity_input.setRange(1, 1000)
        self.quantity_input.setValue(1)
        form_layout.addWidget(self.quantity_input)
        
        # Selling Price
        self.price_input = QDoubleSpinBox()
        self.price_input.setPrefix="₹ "
        self.price_input.setRange(0, 10000)
        self.price_input.setValue(0)
        form_layout.addWidget(self.price_input)
        
        # Add Sale Button
        self.add_button = QPushButton("Add Sale")
        self.add_button.clicked.connect(self.add_sale)
        form_layout.addWidget(self.add_button)
        
        main_layout.addLayout(form_layout)
        
        # Sales Table
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "ID", "Product", "Quantity", "Price", "Total", "Profit"
        ])
        self.table.setColumnWidth(0, 50)
        self.table.setColumnWidth(1, 200)
        self.table.setColumnWidth(2, 80)
        self.table.setColumnWidth(3, 80)
        self.table.setColumnWidth(4, 80)
        self.table.setColumnWidth(5, 80)
        main_layout.addWidget(self.table)
        
        self.setLayout(main_layout)
        self.load_products()
        self.load_sales()
        
    def add_sale(self):
        product_id = self.product_combo.currentData()
        quantity = self.quantity_input.value()
        selling_price = self.price_input.value()
        
        if not product_id:
            return
            
        with Session(get_db()) as db:
            product = db.query(Product).filter(Product.id == product_id).first()
            if product.stock_quantity < quantity:
                return
                
            total_amount = quantity * selling_price
            profit = (selling_price - product.purchase_cost) * quantity
            
            sale = Sale(
                product_id=product_id,
                quantity=quantity,
                selling_price=selling_price,
                total_amount=total_amount,
                profit=profit
            )
            db.add(sale)
            
            # Update stock
            product.stock_quantity -= quantity
            db.commit()
            
        self.load_sales()
        self.clear_form()
        
    def load_products(self):
        from sqlalchemy import select
        with get_connection() as conn:
            products = conn.execute(select(Product)).all()
            self.product_combo.clear()
            self.product_combo.addItem("Select Product")
            for product in products:
                self.product_combo.addItem(f"{product.name} ({product.company.name})", product.id)
                
    def load_sales(self):
        from sqlalchemy import select
        with get_connection() as conn:
            sales = conn.execute(select(Sale)).all()
            self.table.setRowCount(len(sales))
            for row, sale in enumerate(sales):
                self.table.setItem(row, 0, QTableWidgetItem(str(sale.id)))
                self.table.setItem(row, 1, QTableWidgetItem(sale.product.name))
                self.table.setItem(row, 2, QTableWidgetItem(str(sale.quantity)))
                self.table.setItem(row, 3, QTableWidgetItem(f"₹{sale.selling_price}"))
                self.table.setItem(row, 4, QTableWidgetItem(f"₹{sale.total_amount}"))
                self.table.setItem(row, 5, QTableWidgetItem(f"₹{sale.profit}"))
                
    def clear_form(self):
        self.product_combo.setCurrentIndex(0)
        self.quantity_input.setValue(1)
        self.price_input.setValue(0)

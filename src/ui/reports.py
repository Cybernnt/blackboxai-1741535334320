from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem, QDateEdit
from PyQt6.QtCore import QDate
from src.database.db import get_db
from src.models.sales import Sale
from sqlalchemy.orm import Session
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
import os

class Reports(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        # Main layout
        main_layout = QVBoxLayout()
        
        # Date Range Selection
        date_layout = QHBoxLayout()
        
        self.start_date = QDateEdit()
        self.start_date.setDate(QDate.currentDate().addMonths(-1))
        self.start_date.setCalendarPopup(True)
        date_layout.addWidget(self.start_date)
        
        self.end_date = QDateEdit()
        self.end_date.setDate(QDate.currentDate())
        self.end_date.setCalendarPopup(True)
        date_layout.addWidget(self.end_date)
        
        self.generate_button = QPushButton("Generate Report")
        self.generate_button.clicked.connect(self.generate_report)
        date_layout.addWidget(self.generate_button)
        
        main_layout.addLayout(date_layout)
        
        # Report Table
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels([
            "Date", "Product", "Quantity", "Total", "Profit"
        ])
        self.table.setColumnWidth(0, 100)
        self.table.setColumnWidth(1, 200)
        self.table.setColumnWidth(2, 80)
        self.table.setColumnWidth(3, 80)
        self.table.setColumnWidth(4, 80)
        main_layout.addWidget(self.table)
        
        self.setLayout(main_layout)
        
    def generate_report(self):
        start_date = self.start_date.date().toPyDate()
        end_date = self.end_date.date().toPyDate()
        
        with Session(get_db()) as db:
            sales = db.query(Sale).filter(
                Sale.sale_date >= start_date,
                Sale.sale_date <= end_date
            ).all()
            
            self.table.setRowCount(len(sales))
            for row, sale in enumerate(sales):
                self.table.setItem(row, 0, QTableWidgetItem(sale.sale_date.strftime("%Y-%m-%d")))
                self.table.setItem(row, 1, QTableWidgetItem(sale.product.name))
                self.table.setItem(row, 2, QTableWidgetItem(str(sale.quantity)))
                self.table.setItem(row, 3, QTableWidgetItem(f"₹{sale.total_amount}"))
                self.table.setItem(row, 4, QTableWidgetItem(f"₹{sale.profit}"))
                
            # Generate PDF
            self.generate_pdf(sales, start_date, end_date)
            
    def generate_pdf(self, sales, start_date, end_date):
        file_name = f"sales_report_{start_date}_{end_date}.pdf"
        path = os.path.join("reports", file_name)
        os.makedirs("reports", exist_ok=True)
        
        c = canvas.Canvas(path, pagesize=A4)
        width, height = A4
        
        # Title
        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, height - 50, f"Sales Report: {start_date} to {end_date}")
        
        # Table Data
        data = [["Date", "Product", "Quantity", "Total", "Profit"]]
        total_sales = 0
        total_profit = 0
        
        for sale in sales:
            data.append([
                sale.sale_date.strftime("%Y-%m-%d"),
                sale.product.name,
                str(sale.quantity),
                f"₹{sale.total_amount}",
                f"₹{sale.profit}"
            ])
            total_sales += sale.total_amount
            total_profit += sale.profit
            
        # Add totals row
        data.append(["Total", "", "", f"₹{total_sales}", f"₹{total_profit}"])
        
        # Create table
        table = Table(data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -2), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        # Draw table
        table.wrapOn(c, width - 100, height - 100)
        table.drawOn(c, 50, height - 300)
        
        c.save()

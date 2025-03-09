from PyQt6.QtWidgets import QMainWindow, QTabWidget
from src.ui.company_management import CompanyManagement
from src.ui.product_management import ProductManagement
from src.ui.sales_management import SalesManagement
from src.ui.reports import Reports

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Fitness Store Inventory Management")
        self.setGeometry(100, 100, 1200, 800)
        
        # Create tab widget
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        
        # Add tabs
        self.company_tab = CompanyManagement()
        self.product_tab = ProductManagement()
        self.sales_tab = SalesManagement()
        self.reports_tab = Reports()
        
        self.tabs.addTab(self.company_tab, "Company Management")
        self.tabs.addTab(self.product_tab, "Product Management")
        self.tabs.addTab(self.sales_tab, "Sales Management")
        self.tabs.addTab(self.reports_tab, "Reports")

import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QGuiApplication
from src.ui.main_window import MainWindow
from src.database.db import init_db, get_connection
from sqlalchemy import select
from src.models.company import Company
from src.models.product import Product
from src.models.sales import Sale

def print_menu():
    print("\nFitness Store Inventory Management")
    print("1. List Companies")
    print("2. List Products")
    print("3. List Sales")
    print("4. Exit")
    return input("Select an option: ")

def list_companies():
    print("\nCompanies:")
    print("-" * 50)
    with get_connection() as conn:
        companies = conn.execute(select(Company)).all()
        for company in companies:
            print(f"ID: {company.id}, Name: {company.name}")

def list_products():
    print("\nProducts:")
    print("-" * 50)
    with get_connection() as conn:
        products = conn.execute(select(Product)).all()
        for product in products:
            print(f"ID: {product.id}, Name: {product.name}, Stock: {product.stock_quantity}")

def list_sales():
    print("\nSales:")
    print("-" * 50)
    with get_connection() as conn:
        sales = conn.execute(select(Sale)).all()
        for sale in sales:
            print(f"ID: {sale.id}, Product ID: {sale.product_id}, Quantity: {sale.quantity}, Total: ₹{sale.total_amount}")

def main():
    """Main entry point of the application"""
    # Initialize database
    init_db()
    
    while True:
        choice = print_menu()
        if choice == "1":
            list_companies()
        elif choice == "2":
            list_products()
        elif choice == "3":
            list_sales()
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid option, please try again.")

if __name__ == "__main__":
    main()

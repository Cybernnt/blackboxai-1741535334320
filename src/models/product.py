from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from src.database.db import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    image_path = Column(String)
    hsn_code = Column(String)
    flavor = Column(String)
    weight = Column(Float)  # in grams
    mrp = Column(Float)
    purchase_cost = Column(Float)
    selling_cost = Column(Float)
    expiry_date = Column(Date)
    stock_quantity = Column(Integer, default=0)
    company_id = Column(Integer, ForeignKey("companies.id"))
    category_id = Column(Integer, ForeignKey("categories.id"))
    
    # Relationships
    company = relationship("Company", back_populates="products")
    category = relationship("Category", back_populates="products")
    sales = relationship("Sale", back_populates="product", cascade="all, delete-orphan")

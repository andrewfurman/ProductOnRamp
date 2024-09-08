from sqlalchemy import create_engine, Column, Integer, Text, String, Date, Boolean, DECIMAL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Create a database engine
engine = create_engine(os.environ['DATABASE_URL'])

# Create a base class for declarative models
Base = declarative_base()

# Define the Product model
class Product(Base):
    __tablename__ = 'product'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    url = Column(Text)
    summary_of_benefits = Column(Text)
    line_of_business = Column(Text)

    # New columns
    in_network_individual_deductible = Column(DECIMAL(10,2))
    in_network_family_deductible = Column(DECIMAL(10,2))
    out_of_network_individual_deductible = Column(DECIMAL(10,2))
    out_of_network_family_deductible = Column(DECIMAL(10,2))
    in_network_individual_oop_limit = Column(DECIMAL(10,2))
    in_network_family_oop_limit = Column(DECIMAL(10,2))
    out_of_network_individual_oop_limit = Column(DECIMAL(10,2))
    out_of_network_family_oop_limit = Column(DECIMAL(10,2))
    plan_name = Column(String(255))
    plan_year = Column(Integer)
    plan_status = Column(String(50))
    plan_type = Column(String(50))
    plan_design = Column(String(50))
    metal_level = Column(String(50))
    coverage_type = Column(String(50))
    funding_arrangement = Column(String(50))
    group_size = Column(Integer)
    network_type = Column(String(100))
    effective_date = Column(Date)
    end_date = Column(Date)
    employer_contribution = Column(DECIMAL(10,2))
    actuarial_value = Column(DECIMAL(5,2))
    distribution_channels = Column(String(255))
    provider_network_link = Column(String(255))
    provider_network_phone = Column(Text)
    plan_marketing_name = Column(String(255))
    market_segment = Column(String(100))
    is_hsa_eligible = Column(Boolean)
    deductible_combined_separate = Column(String(50))
    specialist_referral_required = Column(Boolean)
    grandfathered_plan = Column(Boolean)
    coverage_summary = Column(Text)

    def __repr__(self):
        return f"<Product(id={self.id}, name='{self.name or 'None'}', url='{self.url or 'None'}', line_of_business='{self.line_of_business or 'None'}')>"

# Create the table in the database
Base.metadata.create_all(engine)

# Create a session factory
SessionLocal = sessionmaker(bind=engine)
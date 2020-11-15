import datetime
import uuid
import enum

from sqlalchemy import ( 
    Column, 
    Integer, 
    String, 
    DateTime, 
    Numeric,
    ForeignKey
)

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, backref

from database import Base


class Users(Base):
    __tablename__  = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    first_name = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class Metrics(Base):
    __tablename__ = "metrics"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    title = Column(String)
    description = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    

# MUDAR ESSE NOME QUE TÁ UMA MERDA.
class BusinessData(Base):
    __tablename__ = "business_data"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    marketing_cost = Column(Numeric(18, 2))
    customers_per_month = Column(Integer)
    avg_monthly_client_spend = Column(Numeric(18, 2))
    times_customer_buy_per_year = Column(Integer)
    current_active_customers = Column(Integer)
    lost_customers_month = Column(Integer)
    gross_monthly_revenue = Column(Numeric(18, 2))
    total_monthly_expenses = Column(Numeric(18, 2))
    net_profit_month = Column(Numeric(18, 2))
    id_user = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class AnalysisResults(Base):
    __tablename__ = "analysis_results"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    result_cac = Column(Numeric(18, 2))
    result_cac_message = Column(String)
    result_ltv = Column(Numeric(18, 2))
    result_ltv_message = Column(String)
    result_ratio = Column(Numeric(18, 2))
    result_ratio_message = Column(String)
    result_churn = Column(Numeric(18, 2))
    result_churn_message = Column(String)
    result_operational_margin = Column(Numeric(18, 2))
    result_operational_margin_message = Column(String)
    result_profitability = Column(Numeric(18, 2))
    result_profitability_message = Column(String)
    id_user = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    id_business_data = Column(UUID(as_uuid=True), ForeignKey("business_data.id"))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
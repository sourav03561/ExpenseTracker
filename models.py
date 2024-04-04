from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
class IncomeExpenses(db.Model):
    __tablename__ = "expenses"
    id = db.Column(db.Integer, primary_key=True)
    types = db.Column(db.String(30), default='income', nullable=False)
    category = db.Column(db.String(30), nullable=False, default='rent')
    date = db.Column(db.DateTime, nullable=False, default= datetime.utcnow)
    amount = db.Column(db.Integer, nullable=False)
    

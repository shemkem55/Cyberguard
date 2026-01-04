from sqlalchemy.orm import Session
from . import models

def get_assets(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Asset).offset(skip).limit(limit).all()

def create_asset(db: Session, asset_data: dict):
    db_asset = models.Asset(**asset_data)
    db.add(db_asset)
    db.commit()
    db.refresh(db_asset)
    return db_asset

def get_vulnerabilities(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Vulnerability).offset(skip).limit(limit).all()

def create_vulnerability(db: Session, vuln_data: dict):
    db_vuln = models.Vulnerability(**vuln_data)
    db.add(db_vuln)
    db.commit()
    db.refresh(db_vuln)
    return db_vuln

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.config import settings

connect_args = {"check_same_thread": False} if settings.DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(
    settings.DATABASE_URL,
    connect_args=connect_args,
    echo=False,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def init_db():
    try:
        Base.metadata.create_all(bind=engine)
    except Exception as e:
        import logging
        logging.getLogger("database").warning(f"Database init warning (non-fatal): {e}")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def seed_securebank_demo():
    """Idempotently seed the SecureBank demo brand, official apps, and aliases."""
    from app import models_app
    from app.database import SessionLocal

    db = SessionLocal()
    try:
        brand = db.query(models_app.Brand).filter(models_app.Brand.name == "SecureBank").first()
        if brand is None:
            brand = models_app.Brand(
                name="SecureBank",
                website="https://securebank.com",
                logo_url="https://via.placeholder.com/120x120/1a56db/ffffff?text=SB",
                aliases=["Secure Bank", "SecureBank Financial", "SBFS"],
                keywords=["banking", "fintech", "digital banking", "secure payments", "financial services"],
                product_names=["SecureBank Mobile", "SecureBank Business"],
                service_names=["Mobile Banking", "Business Banking"],
                official_developer_names=["SecureBank Financial Services Inc."],
                official_email_domains=["securebank.com"],
            )
            db.add(brand)
            db.commit()
            db.refresh(brand)

        official_apps = [
            {
                "name": "SecureBank Mobile",
                "package_id": "com.securebank.mobile",
                "bundle_id": None,
                "store_url": "https://play.google.com/store/apps/details?id=com.securebank.mobile",
                "developer_name": "SecureBank Financial Services Inc.",
                "developer_website": "https://securebank.com",
                "developer_email": "support@securebank.com",
                "platform": models_app.AppPlatform.ANDROID,
                "store": models_app.AppStoreSource.DEMO,
                "icon_url": "https://via.placeholder.com/80x80/1a56db/ffffff?text=SB",
                "description": "Official mobile banking app for SecureBank customers. Manage accounts, transfer funds, and monitor transactions securely.",
            },
            {
                "name": "SecureBank Business",
                "package_id": "com.securebank.business",
                "bundle_id": None,
                "store_url": "https://apps.apple.com/app/securebank-business/id123456789",
                "developer_name": "SecureBank Financial Services Inc.",
                "developer_website": "https://securebank.com",
                "developer_email": "support@securebank.com",
                "platform": models_app.AppPlatform.IOS,
                "store": models_app.AppStoreSource.DEMO,
                "icon_url": "https://via.placeholder.com/80x80/0d9488/ffffff?text=SB",
                "description": "Business banking solution for SecureBank commercial clients. Multi-user access, approval workflows, and advanced reporting.",
            },
        ]
        for app_data in official_apps:
            existing = db.query(models_app.OfficialMobileApp).filter(
                models_app.OfficialMobileApp.brand_id == brand.id,
                models_app.OfficialMobileApp.package_id == app_data["package_id"],
            ).first()
            if existing is None:
                official_app = models_app.OfficialMobileApp(brand_id=brand.id, **app_data)
                db.add(official_app)
        db.commit()
    finally:
        db.close()

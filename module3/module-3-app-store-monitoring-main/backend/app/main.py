from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base, SessionLocal
import app.models_app  # Import to ensure tables are created
from app.routers import brands, apps, scans, detection
from app import models_app

# Create database tables
Base.metadata.create_all(bind=engine)


def seed_securebank_demo():
    """Idempotently seed the SecureBank demo brand, official apps, and aliases."""
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

        # Seed official mobile apps (idempotent by package_id)
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


seed_securebank_demo()

app = FastAPI(
    title="Module 3: App Store Monitoring & Suspicious App Detection",
    description="Digital Risk Protection Platform - Module 3",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(brands.router, prefix="/api/brands", tags=["brands"])
app.include_router(apps.router, prefix="/api/apps", tags=["apps"])
app.include_router(scans.router, prefix="/api/scans", tags=["scans"])
app.include_router(detection.router, prefix="/api/detection", tags=["detection"])

@app.get("/")
async def root():
    return {"message": "Module 3: App Store Monitoring & Suspicious App Detection API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "module": "3", "service": "app_store_monitoring"}
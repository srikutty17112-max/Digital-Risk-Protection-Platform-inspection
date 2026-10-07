from fastapi.testclient import TestClient
from app.main import app


class TestHealthEndpoints:
    def test_root(self, client: TestClient):
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["service"] == "BrandShield Social Media Monitoring & Impersonation Detection"
        assert data["module"] == 2
        assert data["docs"] == "/docs"
        assert data["health"] == "/health"

    def test_health(self, client: TestClient):
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "social-media-monitoring"
        assert "version" in data
        assert "demo_mode" in data


class TestCandidatesAPI:
    def test_list_candidates_empty(self, client: TestClient):
        response = client.get("/api/candidates?brand_id=NONEXISTENT")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 0
        assert data["candidates"] == []

    def test_add_candidate(self, client: TestClient):
        payload = {
            "candidate_id": "TEST-CANDIDATE-001",
            "brand_id": "TESTBRAND",
            "platform": "instagram",
            "username": "testbrand_official",
            "display_name": "Test Brand Official",
            "profile_url": "https://instagram.com/testbrand_official",
            "bio": "Official test brand account",
            "profile_image_url": "https://demo-assets.brandshield.io/testbrand/logo.png",
            "logo_image_url": "https://demo-assets.brandshield.io/testbrand/logo.png",
            "followers_count": 10000,
            "following_count": 100,
            "verification_status": "verified",
            "external_links": ["https://testbrand.com"],
            "contact_information": {"email": "hello@testbrand.com"},
            "collection_source": "DEMO",
        }
        response = client.post("/api/candidates", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["candidate_id"] == "TEST-CANDIDATE-001"
        assert data["username"] == "testbrand_official"

    def test_get_candidate_not_found(self, client: TestClient):
        response = client.get("/api/candidates/NONEXISTENT")
        assert response.status_code == 404

    def test_get_candidate(self, client: TestClient):
        payload = {
            "candidate_id": "TEST-CANDIDATE-002",
            "brand_id": "TESTBRAND",
            "platform": "instagram",
            "username": "testbrand_support",
            "display_name": "Test Brand Support",
            "profile_url": "https://instagram.com/testbrand_support",
            "bio": "Support account",
            "profile_image_url": "https://demo-assets.brandshield.io/testbrand/logo.png",
            "logo_image_url": "https://demo-assets.brandshield.io/testbrand/logo.png",
            "followers_count": 1000,
            "following_count": 200,
            "verification_status": "none",
            "external_links": ["https://testbrand-support.com"],
            "contact_information": {"email": "support@testbrand-support.com"},
            "collection_source": "DEMO",
        }
        client.post("/api/candidates", json=payload)
        response = client.get("/api/candidates/TEST-CANDIDATE-002")
        assert response.status_code == 200
        data = response.json()
        assert data["candidate_id"] == "TEST-CANDIDATE-002"


class TestScanAPI:
    def test_run_scan(self, client: TestClient):
        payload = {
            "brand_id": "KAMPUSVC",
            "platforms": ["instagram"],
            "use_demo_data": True,
        }
        response = client.post("/api/scan", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert "job_id" in data
        assert data["brand_id"] == "KAMPUSVC"
        assert data["status"] in ["PENDING", "RUNNING", "COMPLETED"]

    def test_get_scan_status(self, client: TestClient):
        payload = {
            "brand_id": "KAMPUSVC",
            "platforms": ["instagram"],
            "use_demo_data": True,
        }
        response = client.post("/api/scan", json=payload)
        data = response.json()
        job_id = data["job_id"]

        response = client.get(f"/api/scan/{job_id}")
        assert response.status_code == 200
        assert response.json()["job_id"] == job_id

    def test_get_scan_status_not_found(self, client: TestClient):
        response = client.get("/api/scan/NONEXISTENT")
        assert response.status_code == 404

    def test_get_scan_history(self, client: TestClient):
        payload = {
            "brand_id": "KAMPUSVC",
            "platforms": ["instagram"],
            "use_demo_data": True,
        }
        client.post("/api/scan", json=payload)

        response = client.get("/api/scan/history/KAMPUSVC")
        assert response.status_code == 200
        assert isinstance(response.json(), list)


class TestThreatsAPI:
    def test_get_threats_empty(self, client: TestClient):
        response = client.get("/api/threats?brand_id=NONEXISTENT")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 0
        assert data["threats"] == []

    def test_get_threats_after_scan(self, client: TestClient):
        payload = {
            "brand_id": "KAMPUSVC",
            "platforms": ["instagram"],
            "use_demo_data": True,
        }
        client.post("/api/scan", json=payload)

        response = client.get("/api/threats?brand_id=KAMPUSVC")
        assert response.status_code == 200
        data = response.json()
        assert "total" in data
        assert "threats" in data
        assert data["page"] == 1

    def test_get_threats_excludes_official_by_default(self, client: TestClient):
        payload = {
            "brand_id": "KAMPUSVC",
            "platforms": ["instagram"],
            "use_demo_data": True,
        }
        client.post("/api/scan", json=payload)

        response = client.get("/api/threats?brand_id=KAMPUSVC")
        data = response.json()
        for threat in data["threats"]:
            assert threat["classification"] != "OFFICIAL"

    def test_get_threats_includes_official_when_requested(self, client: TestClient):
        payload = {
            "brand_id": "KAMPUSVC",
            "platforms": ["instagram"],
            "use_demo_data": True,
        }
        client.post("/api/scan", json=payload)

        response = client.get("/api/threats?brand_id=KAMPUSVC&include_official=true")
        data = response.json()
        has_official = any(t["classification"] == "OFFICIAL" for t in data["threats"])
        assert has_official is True

    def test_full_scan_creates_detections(self, client: TestClient):
        payload = {
            "brand_id": "KAMPUSVC",
            "platforms": ["instagram"],
            "use_demo_data": True,
        }
        response = client.post("/api/scan", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["brand_id"] == "KAMPUSVC"
        assert data["status"] == "COMPLETED"
        assert data["total_candidates"] > 0

        response = client.get(f"/api/threats?brand_id=KAMPUSVC")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] > 0
        assert len(data["threats"]) > 0
        for threat in data["threats"]:
            assert "risk_score" in threat
            assert "confidence" in threat
            assert "reasons" in threat
            assert len(threat["reasons"]) > 0

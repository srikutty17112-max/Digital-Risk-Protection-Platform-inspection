import { useState, useEffect } from 'react';
import { api } from '../api/client';
import type { SocialThreat, SocialScanJobResponse } from '../types/api';

export default function DashboardPage() {
  const [brandId, setBrandId] = useState('SECUREBANK');
  const [threats, setThreats] = useState<SocialThreat[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [scanResult, setScanResult] = useState<SocialScanJobResponse | null>(null);
  const [scanLoading, setScanLoading] = useState(false);

  const load = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await api.getThreats({
        brand_id: brandId.trim(),
        page_size: 100,
        include_official: false,
      });
      setThreats(data.threats);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load dashboard data');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    load();
  }, [brandId]);

  const runScan = async () => {
    setScanLoading(true);
    setScanResult(null);
    setError(null);
    try {
      const result = await api.runScan({
        brand_id: brandId.trim(),
        platforms: ['instagram', 'facebook', 'x_twitter', 'linkedin', 'youtube', 'tiktok'],
        use_demo_data: true,
      });
      setScanResult(result);
      load();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Scan failed');
    } finally {
      setScanLoading(false);
    }
  };

  const totalDetections = threats.length;
  const highRiskCount = threats.filter((t) => t.risk_level === 'HIGH' || t.risk_level === 'CRITICAL').length;
  const avgRiskScore = totalDetections > 0 ? threats.reduce((sum, t) => sum + t.risk_score, 0) / totalDetections : 0;
  const recentThreats = threats.slice(0, 10);

  const riskColor = (level: string) => {
    switch (level) {
      case 'CRITICAL':
        return 'risk-critical';
      case 'HIGH':
        return 'risk-high';
      case 'MEDIUM':
        return 'risk-medium';
      case 'LOW':
        return 'risk-low';
      default:
        return '';
    }
  };

  return (
    <div className="page">
      <h1>Dashboard</h1>

      <div className="card">
        <div className="field">
          <label>Brand ID</label>
          <input
            type="text"
            value={brandId}
            onChange={(e) => setBrandId(e.target.value)}
            placeholder="e.g. SECUREBANK"
          />
        </div>
        <div className="actions">
          <button onClick={load} disabled={loading}>
            {loading ? 'Loading...' : 'Refresh'}
          </button>
          <button className="primary" onClick={runScan} disabled={scanLoading || !brandId.trim()}>
            {scanLoading ? 'Running Scan...' : 'Run Scan'}
          </button>
        </div>
      </div>

      {error && <div className="error">{error}</div>}

      {scanResult && (
        <div className="card">
          <h2>Scan Result</h2>
          <div className="grid">
            <div>
              <strong>Job ID</strong>
              <div>{scanResult.job_id}</div>
            </div>
            <div>
              <strong>Status</strong>
              <div>{scanResult.status}</div>
            </div>
            <div>
              <strong>Candidates</strong>
              <div>
                {scanResult.processed_candidates} / {scanResult.total_candidates}
              </div>
            </div>
            <div>
              <strong>Threats Found</strong>
              <div>{scanResult.threats_found}</div>
            </div>
            <div>
              <strong>Official Accounts</strong>
              <div>{scanResult.official_accounts_found}</div>
            </div>
          </div>
          {scanResult.status === 'COMPLETED' && (
            <div className="actions" style={{ marginTop: 12 }}>
              <a href="#/detections">View Detections</a>
            </div>
          )}
          {scanResult.error_message && (
            <div className="error" style={{ marginTop: 12 }}>
              {scanResult.error_message}
            </div>
          )}
        </div>
      )}

      <div className="summary-grid">
        <div className="summary-card">
          <div className="summary-label">Total Detections</div>
          <div className="summary-value">{totalDetections}</div>
        </div>
        <div className="summary-card">
          <div className="summary-label">High Risk</div>
          <div className="summary-value high-risk">{highRiskCount}</div>
        </div>
        <div className="summary-card">
          <div className="summary-label">Avg Risk Score</div>
          <div className="summary-value">{avgRiskScore.toFixed(1)}</div>
        </div>
      </div>

      <div className="card">
        <h2>Recent Detections</h2>
        {recentThreats.length === 0 ? (
          <p>No detections found.</p>
        ) : (
          <div className="table-wrap">
            <table className="table">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Platform</th>
                  <th>Username</th>
                  <th>Risk Score</th>
                  <th>Risk Level</th>
                  <th>Confidence</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                {recentThreats.map((threat) => (
                  <tr key={threat.id}>
                    <td>{threat.id}</td>
                    <td>{threat.platform}</td>
                    <td>{threat.candidate.username || '-'}</td>
                    <td>{threat.risk_score.toFixed(2)}</td>
                    <td>
                      <span className={`badge ${riskColor(threat.risk_level)}`}>{threat.risk_level}</span>
                    </td>
                    <td>{(threat.confidence * 100).toFixed(0)}%</td>
                    <td>{threat.status}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}

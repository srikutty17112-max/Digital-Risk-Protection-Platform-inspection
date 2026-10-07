import { useState } from 'react';
import { api } from '../api/client';
import type { SocialScanJobResponse, SocialScanRequest, Platform } from '../types/api';

export default function ScansPage() {
  const [brandId, setBrandId] = useState('SECUREBANK');
  const [platforms, setPlatforms] = useState<Platform[]>([]);
  const [useDemo, setUseDemo] = useState(true);
  const [job, setJob] = useState<SocialScanJobResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const platformOptions: Platform[] = [
    'instagram', 'facebook', 'x_twitter', 'linkedin', 'youtube', 'tiktok',
  ];

  const togglePlatform = (p: Platform) => {
    setPlatforms((prev) => (prev.includes(p) ? prev.filter((x) => x !== p) : [...prev, p]));
  };

  const runScan = async () => {
    setLoading(true);
    setError(null);
    setJob(null);
    try {
      const payload: SocialScanRequest = {
        brand_id: brandId.trim(),
        platforms: platforms.length > 0 ? platforms : undefined,
        use_demo_data: useDemo,
      };
      const result = await api.runScan(payload);
      setJob(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Scan failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page">
      <h1>Social Scan</h1>

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

        <div className="field">
          <label>Platforms</label>
          <div className="checkbox-group">
            {platformOptions.map((p) => (
              <label key={p} className="checkbox-label">
                <input
                  type="checkbox"
                  checked={platforms.includes(p)}
                  onChange={() => togglePlatform(p)}
                />
                {p.replace('_', ' ')}
              </label>
            ))}
          </div>
        </div>

        <div className="field">
          <label className="checkbox-label">
            <input
              type="checkbox"
              checked={useDemo}
              onChange={(e) => setUseDemo(e.target.checked)}
            />
            Use demo data
          </label>
        </div>

        <button onClick={runScan} disabled={loading || !brandId.trim()}>
          {loading ? 'Running...' : 'Run Scan'}
        </button>
      </div>

      {error && <div className="error">{error}</div>}

      {job && (
        <div className="card">
          <h2>Scan Job</h2>
          <div className="grid">
            <div>
              <strong>Job ID</strong>
              <div>{job.job_id}</div>
            </div>
            <div>
              <strong>Status</strong>
              <div>{job.status}</div>
            </div>
            <div>
              <strong>Brand</strong>
              <div>{job.brand_id}</div>
            </div>
            <div>
              <strong>Candidates</strong>
              <div>
                {job.processed_candidates} / {job.total_candidates}
              </div>
            </div>
            <div>
              <strong>Threats</strong>
              <div>{job.threats_found}</div>
            </div>
            <div>
              <strong>Official Accounts</strong>
              <div>{job.official_accounts_found}</div>
            </div>
            {job.error_message && (
              <div className="error">
                <strong>Error</strong>
                <div>{job.error_message}</div>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}

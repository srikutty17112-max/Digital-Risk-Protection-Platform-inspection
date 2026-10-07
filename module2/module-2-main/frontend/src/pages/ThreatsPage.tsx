import { useState, useEffect } from 'react';
import { api } from '../api/client';
import type { SocialThreat, ThreatStatus } from '../types/api';

export default function ThreatsPage() {
  const [brandId, setBrandId] = useState('SECUREBANK');
  const [threats, setThreats] = useState<SocialThreat[]>([]);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(1);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const load = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await api.getThreats({
        brand_id: brandId.trim(),
        page,
        page_size: 20,
        include_official: false,
      });
      setThreats(data.threats);
      setTotal(data.total);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load threats');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    load();
  }, [brandId, page]);

  const updateStatus = async (threatId: string, newStatus: ThreatStatus) => {
    try {
      await api.updateThreatStatus(threatId, newStatus);
      load();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to update status');
    }
  };

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
      <h1>Threats</h1>

      <div className="card">
        <div className="field">
          <label>Brand ID</label>
          <input
            type="text"
            value={brandId}
            onChange={(e) => {
              setBrandId(e.target.value);
              setPage(1);
            }}
            placeholder="e.g. SECUREBANK"
          />
        </div>
        <button onClick={load} disabled={loading}>
          {loading ? 'Loading...' : 'Refresh'}
        </button>
      </div>

      {error && <div className="error">{error}</div>}

      <div className="card">
        <h2>Detections ({total})</h2>
        {threats.length === 0 && <p>No threats found.</p>}
        {threats.map((threat) => (
          <div key={threat.id} className="threat-item">
            <div className="threat-header">
              <strong>{threat.id}</strong>
              <span className={`badge ${riskColor(threat.risk_level)}`}>{threat.risk_level}</span>
              <span className="badge">{threat.classification}</span>
            </div>
            <div className="grid">
              <div>
                <strong>Platform</strong>
                <div>{threat.platform}</div>
              </div>
              <div>
                <strong>Username</strong>
                <div>{threat.candidate.username || '-'}</div>
              </div>
              <div>
                <strong>Display Name</strong>
                <div>{threat.candidate.display_name || '-'}</div>
              </div>
              <div>
                <strong>Risk Score</strong>
                <div>{threat.risk_score.toFixed(2)}</div>
              </div>
              <div>
                <strong>Confidence</strong>
                <div>{(threat.confidence * 100).toFixed(0)}%</div>
              </div>
              <div>
                <strong>Status</strong>
                <div>{threat.status}</div>
              </div>
            </div>
            {threat.lookalike.detected && (
              <div className="lookalike">
                <strong>Lookalike:</strong> {threat.lookalike.pattern} ({threat.lookalike.similarity?.toFixed(2)})
                {threat.lookalike.explanation && <div className="muted">{threat.lookalike.explanation}</div>}
              </div>
            )}
            <div className="reasons">
              <strong>Reasons:</strong>
              <ul>
                {threat.reasons.map((r, i) => (
                  <li key={i}>{r}</li>
                ))}
              </ul>
            </div>
            <div className="actions">
              {(['NEW', 'REVIEWED', 'DISMISSED', 'CONFIRMED', 'ESCALATED'] as ThreatStatus[]).map((s) => (
                <button key={s} onClick={() => updateStatus(threat.id, s)} disabled={threat.status === s}>
                  {s}
                </button>
              ))}
            </div>
          </div>
        ))}
      </div>

      {total > 20 && (
        <div className="pagination">
          <button onClick={() => setPage((p) => Math.max(1, p - 1))} disabled={page === 1}>
            Prev
          </button>
          <span>
            Page {page} of {Math.ceil(total / 20)}
          </span>
          <button onClick={() => setPage((p) => Math.min(Math.ceil(total / 20), p + 1))} disabled={page >= Math.ceil(total / 20)}>
            Next
          </button>
        </div>
      )}
    </div>
  );
}

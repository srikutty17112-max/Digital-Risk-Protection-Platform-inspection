import { useState, useEffect } from 'react';
import { api } from '../api/client';
import type { SocialThreat, RiskLevel, Platform, ThreatStatus } from '../types/api';

export default function DetectionsPage() {
  const [brandId, setBrandId] = useState('SECUREBANK');
  const [threats, setThreats] = useState<SocialThreat[]>([]);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(1);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [selectedThreat, setSelectedThreat] = useState<SocialThreat | null>(null);
  const [riskFilter, setRiskFilter] = useState<RiskLevel | ''>('');
  const [platformFilter, setPlatformFilter] = useState<Platform | ''>('');
  const [statusFilter, setStatusFilter] = useState<ThreatStatus | ''>('');

  const platformOptions: Platform[] = [
    'instagram', 'facebook', 'x_twitter', 'linkedin', 'youtube', 'tiktok',
  ];

  const statusOptions: ThreatStatus[] = [
    'NEW', 'REVIEWED', 'DISMISSED', 'CONFIRMED', 'ESCALATED',
  ];

  const load = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await api.getThreats({
        brand_id: brandId.trim(),
        risk_level: riskFilter || undefined,
        status: statusFilter || undefined,
        include_official: false,
        page,
        page_size: 20,
      });

      let filtered = data.threats;
      if (platformFilter) {
        filtered = filtered.filter((t) => t.platform === platformFilter);
      }

      setThreats(filtered);
      setTotal(data.total);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load detections');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    load();
  }, [brandId, page]);

  useEffect(() => {
    setPage(1);
  }, [riskFilter, platformFilter, statusFilter]);

  const updateStatus = async (threatId: string, newStatus: ThreatStatus) => {
    try {
      await api.updateThreatStatus(threatId, newStatus);
      load();
      if (selectedThreat && selectedThreat.id === threatId) {
        setSelectedThreat({ ...selectedThreat, status: newStatus });
      }
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

  const confidencePercent = (confidence: number) => `${(confidence * 100).toFixed(0)}%`;

  const SignalBar = ({ label, value, max = 100, inverse = false }: { label: string; value?: number; max?: number; inverse?: boolean }) => {
    if (value === undefined || value === null) return null;
    const pct = inverse ? ((max - value) / max) * 100 : (value / max) * 100;
    const color = inverse ? (pct > 50 ? 'signal-high' : 'signal-low') : (pct > 70 ? 'signal-high' : pct > 40 ? 'signal-medium' : 'signal-low');
    return (
      <div className="signal-row">
        <div className="signal-label">{label}</div>
        <div className="signal-bar">
          <div className={`signal-fill ${color}`} style={{ width: `${Math.min(100, pct)}%` }} />
        </div>
        <div className="signal-value">{value.toFixed(2)}</div>
      </div>
    );
  };

  return (
    <div className="page">
      <h1>Detections</h1>

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
        <div className="filter-group">
          <div className="field">
            <label>Risk Level</label>
            <select value={riskFilter} onChange={(e) => setRiskFilter(e.target.value as RiskLevel | '')}>
              <option value="">All</option>
              <option value="LOW">Low</option>
              <option value="MEDIUM">Medium</option>
              <option value="HIGH">High</option>
              <option value="CRITICAL">Critical</option>
            </select>
          </div>
          <div className="field">
            <label>Platform</label>
            <select value={platformFilter} onChange={(e) => setPlatformFilter(e.target.value as Platform | '')}>
              <option value="">All</option>
              {platformOptions.map((p) => (
                <option key={p} value={p}>{p.replace('_', ' ')}</option>
              ))}
            </select>
          </div>
          <div className="field">
            <label>Status</label>
            <select value={statusFilter} onChange={(e) => setStatusFilter(e.target.value as ThreatStatus | '')}>
              <option value="">All</option>
              {statusOptions.map((s) => (
                <option key={s} value={s}>{s}</option>
              ))}
            </select>
          </div>
        </div>
        <button onClick={load} disabled={loading}>
          {loading ? 'Loading...' : 'Refresh'}
        </button>
      </div>

      {error && <div className="error">{error}</div>}

      <div className="card">
        <h2>Detections ({total})</h2>
        {threats.length === 0 && <p>No detections found.</p>}
        {threats.map((threat) => (
          <div key={threat.id} className="detection-item">
            <div className="threat-header">
              <strong>{threat.id}</strong>
              <span className={`badge ${riskColor(threat.risk_level)}`}>{threat.risk_level}</span>
              <span className="badge">{threat.classification}</span>
              <span className="badge">{threat.platform}</span>
              <span className="badge">{threat.status}</span>
            </div>
            <div className="grid">
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
                <div>{confidencePercent(threat.confidence)}</div>
              </div>
            </div>
            <div className="actions">
              <button onClick={() => setSelectedThreat(threat)}>
                {selectedThreat?.id === threat.id ? 'Hide Details' : 'View Details'}
              </button>
              {statusOptions.map((s) => (
                <button key={s} onClick={() => updateStatus(threat.id, s)} disabled={threat.status === s}>
                  {s}
                </button>
              ))}
            </div>

            {selectedThreat?.id === threat.id && (
              <div className="detail-panel">
                <h3>Signals</h3>
                <SignalBar label="Name Similarity" value={threat.signals.name_similarity} />
                <SignalBar label="Logo Similarity" value={threat.signals.logo_similarity} />
                <SignalBar label="Branding Similarity" value={threat.signals.branding_similarity} />
                <SignalBar label="External Domain Similarity" value={threat.signals.external_domain_similarity} inverse />

                <h3>Lookalike</h3>
                {threat.lookalike.detected ? (
                  <div className="detail-row">
                    <strong>Pattern:</strong> {threat.lookalike.pattern}
                    {threat.lookalike.similarity !== undefined && (
                      <span> ({(threat.lookalike.similarity * 100).toFixed(0)}%)</span>
                    )}
                    {threat.lookalike.explanation && <div className="muted">{threat.lookalike.explanation}</div>}
                  </div>
                ) : (
                  <p>No lookalike pattern detected.</p>
                )}

                <h3>Official Match</h3>
                <div className="detail-row">
                  <strong>Is Official:</strong> {threat.official_match.is_official ? 'Yes' : 'No'}
                  {threat.official_match.matched_asset_id && <span> (Asset: {threat.official_match.matched_asset_id})</span>}
                  <div>
                    <strong>Match Type:</strong> {threat.official_match.match_type} ({confidencePercent(threat.official_match.confidence)})
                  </div>
                </div>

                <h3>Reasons</h3>
                <ul>
                  {threat.reasons.map((r, i) => (
                    <li key={i}>{r}</li>
                  ))}
                </ul>
              </div>
            )}
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

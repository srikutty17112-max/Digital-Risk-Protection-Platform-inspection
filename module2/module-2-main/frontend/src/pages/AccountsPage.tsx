import { useState, useEffect } from 'react';
import { api } from '../api/client';
import type { SocialCandidate, SocialCandidateCreate, Platform, SocialScanJobResponse } from '../types/api';

export default function AccountsPage() {
  const [brandId, setBrandId] = useState('SECUREBANK');
  const [candidates, setCandidates] = useState<SocialCandidate[]>([]);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(1);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [showForm, setShowForm] = useState(false);
  const [officialIds, setOfficialIds] = useState<Set<string>>(new Set());
  const [scanResult, setScanResult] = useState<SocialScanJobResponse | null>(null);
  const [scanLoading, setScanLoading] = useState(false);

  const [form, setForm] = useState({
    candidate_id: '',
    platform: 'instagram' as Platform,
    username: '',
    display_name: '',
    profile_url: '',
    bio: '',
    profile_image_url: '',
    logo_image_url: '',
    followers_count: '',
    following_count: '',
    verification_status: '',
    external_links: '',
    contact_information: '',
  });

  const load = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await api.getCandidates({
        brand_id: brandId.trim(),
        page,
        page_size: 20,
      });
      setCandidates(data.candidates);
      setTotal(data.total);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load accounts');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    load();
  }, [brandId, page]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    try {
      const payload: SocialCandidateCreate = {
        candidate_id: form.candidate_id,
        brand_id: brandId.trim(),
        platform: form.platform,
        username: form.username || undefined,
        display_name: form.display_name || undefined,
        profile_url: form.profile_url || undefined,
        bio: form.bio || undefined,
        profile_image_url: form.profile_image_url || undefined,
        logo_image_url: form.logo_image_url || undefined,
        followers_count: form.followers_count ? Number(form.followers_count) : undefined,
        following_count: form.following_count ? Number(form.following_count) : undefined,
        verification_status: form.verification_status || undefined,
        external_links: form.external_links ? form.external_links.split('\n').filter(Boolean) : undefined,
        contact_information: form.contact_information ? JSON.parse(form.contact_information) : undefined,
        collection_source: 'DEMO',
      };
      await api.addCandidate(payload);
      setShowForm(false);
      setForm({
        candidate_id: '',
        platform: 'instagram',
        username: '',
        display_name: '',
        profile_url: '',
        bio: '',
        profile_image_url: '',
        logo_image_url: '',
        followers_count: '',
        following_count: '',
        verification_status: '',
        external_links: '',
        contact_information: '',
      });
      load();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to add account');
    }
  };

  const toggleOfficial = (candidateId: string) => {
    setOfficialIds((prev) => {
      const next = new Set(prev);
      if (next.has(candidateId)) {
        next.delete(candidateId);
      } else {
        next.add(candidateId);
      }
      return next;
    });
  };

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

  return (
    <div className="page">
      <h1>Accounts</h1>

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
        <div className="actions">
          <button onClick={load} disabled={loading}>
            {loading ? 'Loading...' : 'Refresh'}
          </button>
          <button onClick={() => setShowForm((v) => !v)}>
            {showForm ? 'Cancel' : 'Add Account'}
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

      {showForm && (
        <div className="card">
          <h2>Add Account</h2>
          <form onSubmit={handleSubmit} className="form">
            <div className="field">
              <label>Candidate ID</label>
              <input
                required
                value={form.candidate_id}
                onChange={(e) => setForm({ ...form, candidate_id: e.target.value })}
              />
            </div>
            <div className="field">
              <label>Platform</label>
              <select
                value={form.platform}
                onChange={(e) => setForm({ ...form, platform: e.target.value as Platform })}
              >
                <option value="instagram">Instagram</option>
                <option value="facebook">Facebook</option>
                <option value="x_twitter">X / Twitter</option>
                <option value="linkedin">LinkedIn</option>
                <option value="youtube">YouTube</option>
                <option value="tiktok">TikTok</option>
              </select>
            </div>
            <div className="field">
              <label>Handle / Username</label>
              <input
                required
                value={form.username}
                onChange={(e) => setForm({ ...form, username: e.target.value })}
                placeholder="e.g. securebank"
              />
            </div>
            <div className="field">
              <label>Display Name</label>
              <input
                required
                value={form.display_name}
                onChange={(e) => setForm({ ...form, display_name: e.target.value })}
                placeholder="e.g. KampusVC"
              />
            </div>
            <div className="field">
              <label>Profile URL</label>
              <input
                value={form.profile_url}
                onChange={(e) => setForm({ ...form, profile_url: e.target.value })}
                placeholder="https://..."
              />
            </div>
            <div className="field">
              <label>Bio</label>
              <textarea value={form.bio} onChange={(e) => setForm({ ...form, bio: e.target.value })} />
            </div>
            <div className="field">
              <label>External Links (one per line)</label>
              <textarea
                rows={3}
                value={form.external_links}
                onChange={(e) => setForm({ ...form, external_links: e.target.value })}
              />
            </div>
            <div className="field">
              <label>Contact Information (JSON)</label>
              <textarea
                rows={2}
                value={form.contact_information}
                onChange={(e) => setForm({ ...form, contact_information: e.target.value })}
                placeholder='{"email": "hello@example.com"}'
              />
            </div>
            <button type="submit">Save Account</button>
          </form>
        </div>
      )}

      <div className="card">
        <h2>Monitored Accounts ({total})</h2>
        {candidates.length === 0 && <p>No accounts found.</p>}
        {candidates.map((c) => {
          const isOfficial = officialIds.has(c.candidate_id);
          return (
            <div key={c.candidate_id} className="account-item">
              <div className="threat-header">
                <strong>{c.candidate_id}</strong>
                <span className="badge">{c.platform}</span>
                <span className={`badge ${isOfficial ? 'official-badge' : 'unofficial-badge'}`}>
                  {isOfficial ? 'Official' : 'Non-Official'}
                </span>
                <span className="badge">{c.collection_source}</span>
              </div>
              <div className="grid">
                <div>
                  <strong>Handle</strong>
                  <div>{c.username || '-'}</div>
                </div>
                <div>
                  <strong>Display Name</strong>
                  <div>{c.display_name || '-'}</div>
                </div>
                <div>
                  <strong>Followers</strong>
                  <div>{c.followers_count ?? '-'}</div>
                </div>
                <div>
                  <strong>Verified</strong>
                  <div>{c.verification_status || '-'}</div>
                </div>
              </div>
              <div className="actions">
                <button onClick={() => toggleOfficial(c.candidate_id)}>
                  {isOfficial ? 'Unmark Official' : 'Mark as Official'}
                </button>
              </div>
              {isOfficial && (
                <div className="official-note">
                  This account is marked as official and will be excluded from impersonation detection.
                </div>
              )}
            </div>
          );
        })}
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

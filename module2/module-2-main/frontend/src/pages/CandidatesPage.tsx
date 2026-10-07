import { useState, useEffect } from 'react';
import { api } from '../api/client';
import type { SocialCandidate, SocialCandidateCreate } from '../types/api';

export default function CandidatesPage() {
  const [brandId, setBrandId] = useState('SECUREBANK');
  const [candidates, setCandidates] = useState<SocialCandidate[]>([]);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(1);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [showForm, setShowForm] = useState(false);

  const [form, setForm] = useState({
    candidate_id: '',
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
      setError(err instanceof Error ? err.message : 'Failed to load candidates');
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
        platform: 'instagram',
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
      setError(err instanceof Error ? err.message : 'Failed to add candidate');
    }
  };

  return (
    <div className="page">
      <h1>Candidates</h1>

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
            {showForm ? 'Cancel' : 'Add Candidate'}
          </button>
        </div>
      </div>

      {error && <div className="error">{error}</div>}

      {showForm && (
        <div className="card">
          <h2>Add Candidate</h2>
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
              <label>Username</label>
              <input value={form.username} onChange={(e) => setForm({ ...form, username: e.target.value })} />
            </div>
            <div className="field">
              <label>Display Name</label>
              <input value={form.display_name} onChange={(e) => setForm({ ...form, display_name: e.target.value })} />
            </div>
            <div className="field">
              <label>Profile URL</label>
              <input value={form.profile_url} onChange={(e) => setForm({ ...form, profile_url: e.target.value })} />
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
            <button type="submit">Save</button>
          </form>
        </div>
      )}

      <div className="card">
        <h2>Monitored Accounts ({total})</h2>
        {candidates.length === 0 && <p>No candidates found.</p>}
        {candidates.map((c) => (
          <div key={c.candidate_id} className="candidate-item">
            <div className="threat-header">
              <strong>{c.candidate_id}</strong>
              <span className="badge">{c.platform}</span>
              <span className="badge">{c.collection_source}</span>
            </div>
            <div className="grid">
              <div>
                <strong>Username</strong>
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

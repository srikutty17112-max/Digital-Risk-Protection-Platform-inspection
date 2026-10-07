import { useState } from 'react';
import type { SocialAccount } from '../types/brand';
import { platformIcons, platformColors, platformLabels, formatUrl } from '../utils/platform';

interface SocialAccountsProps {
  accounts: SocialAccount[];
  onUpdate: (accounts: SocialAccount[]) => void;
}

const PLATFORMS: SocialAccount['platform'][] = ['twitter', 'linkedin', 'facebook', 'instagram', 'youtube'];

export function SocialAccounts({ accounts, onUpdate }: SocialAccountsProps) {
  const [editingId, setEditingId] = useState<string | null>(null);
  const [editForm, setEditForm] = useState<Partial<SocialAccount>>({});

  const handleAdd = (platform: SocialAccount['platform']) => {
    const newAccount: SocialAccount = {
      id: `social-${Date.now()}`,
      platform,
      url: '',
      handle: '',
      verified: false,
    };
    onUpdate([...accounts, newAccount]);
    setEditingId(newAccount.id);
    setEditForm({ platform, url: '', handle: '', verified: false });
  };

  const handleEdit = (account: SocialAccount) => {
    setEditingId(account.id);
    setEditForm({ ...account });
  };

  const handleSave = (id: string) => {
    const updated = accounts.map((a) => (a.id === id ? { ...a, ...editForm } : a));
    onUpdate(updated);
    setEditingId(null);
    setEditForm({});
  };

  const handleCancel = () => {
    setEditingId(null);
    setEditForm({});
  };

  const handleRemove = (id: string) => {
    onUpdate(accounts.filter((a) => a.id !== id));
  };

  const handleChange = (field: keyof SocialAccount, value: string) => {
    setEditForm({ ...editForm, [field]: value });
  };

  const registeredPlatforms = accounts.map((a) => a.platform);
  const availablePlatforms = PLATFORMS.filter((p) => !registeredPlatforms.includes(p));

  return (
    <section className="section-card" aria-labelledby="social-accounts-heading">
      <div className="section-header">
        <h2 id="social-accounts-heading" className="section-title">
          <svg className="section-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <circle cx="12" cy="12" r="10" />
            <path d="M8 14s1.5 2 4 2 4-2 4-2" />
            <line x1="9" y1="9" x2="9.01" y2="9" />
            <line x1="15" y1="9" x2="15.01" y2="9" />
          </svg>
          Official Social Accounts
        </h2>
        <span className="badge badge-trusted">TRUSTED OFFICIAL</span>
      </div>

      <div className="social-accounts-container">
        {accounts.length > 0 ? (
          <div className="accounts-table-wrapper">
            <table className="accounts-table" role="table">
              <thead>
                <tr>
                  <th scope="col">Platform</th>
                  <th scope="col">Handle / URL</th>
                  <th scope="col">Status</th>
                  <th scope="col">Actions</th>
                </tr>
              </thead>
              <tbody>
                {accounts.map((account) => (
                  <tr key={account.id} className={editingId === account.id ? 'editing' : ''}>
                    <td>
                      <div className="platform-cell">
                        <img
                          src={platformIcons[account.platform]}
                          alt=""
                          className="platform-icon"
                          style={{ filter: `drop-shadow(0 0 0 ${platformColors[account.platform]})` }}
                        />
                        <span className="platform-name">{platformLabels[account.platform]}</span>
                      </div>
                    </td>
                    <td>
                      {editingId === account.id ? (
                        <div className="edit-form">
                          <input
                            type="text"
                            className="form-input edit-input"
                            placeholder="Handle (e.g., @securebank)"
                            value={editForm.handle || ''}
                            onChange={(e) => handleChange('handle', e.target.value)}
                          />
                          <input
                            type="url"
                            className="form-input edit-input"
                            placeholder="Full URL"
                            value={editForm.url || ''}
                            onChange={(e) => handleChange('url', e.target.value)}
                          />
                        </div>
                      ) : (
                        <div className="account-info">
                          <div className="handle-row">
                            <code className="handle-code">{account.handle || 'Not set'}</code>
                            {account.verified && (
                              <span className="verified-badge" title="Verified official account">
                                <svg viewBox="0 0 24 24" fill="currentColor" className="verified-icon">
                                  <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z" />
                                </svg>
                              </span>
                            )}
                          </div>
                          <div className="url-row">{formatUrl(account.url)}</div>
                        </div>
                      )}
                    </td>
                    <td>
                      {editingId === account.id ? (
                        <label className="checkbox-label">
                          <input
                            type="checkbox"
                            className="checkbox"
                            checked={editForm.verified || false}
                            onChange={(e) => handleChange('verified', e.target.checked.toString())}
                          />
                          <span>Verified</span>
                        </label>
                      ) : (
                        <span className={`status-badge ${account.verified ? 'verified' : 'unverified'}`}>
                          {account.verified ? 'Verified' : 'Unverified'}
                        </span>
                      )}
                    </td>
                    <td>
                      {editingId === account.id ? (
                        <div className="action-buttons">
                          <button
                            type="button"
                            className="btn btn-primary btn-sm"
                            onClick={() => handleSave(account.id)}
                          >
                            Save
                          </button>
                          <button type="button" className="btn btn-secondary btn-sm" onClick={handleCancel}>
                            Cancel
                          </button>
                        </div>
                      ) : (
                        <div className="action-buttons">
                          <button
                            type="button"
                            className="btn btn-secondary btn-sm"
                            onClick={() => handleEdit(account)}
                          >
                            Edit
                          </button>
                          <button
                            type="button"
                            className="btn btn-danger btn-sm"
                            onClick={() => handleRemove(account.id)}
                          >
                            Remove
                          </button>
                        </div>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <div className="empty-state">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" className="empty-icon">
              <circle cx="12" cy="12" r="10" />
              <path d="M8 14s1.5 2 4 2 4-2 4-2" />
              <line x1="9" y1="9" x2="9.01" y2="9" />
              <line x1="15" y1="9" x2="15.01" y2="9" />
            </svg>
            <h3>No Official Social Accounts Registered</h3>
            <p>Add your brand's official social media accounts to establish the trusted baseline.</p>
          </div>
        )}

        {availablePlatforms.length > 0 && (
          <div className="add-account-section">
            <h4>Add Official Account</h4>
            <div className="platform-buttons">
              {availablePlatforms.map((platform) => (
                <button
                  key={platform}
                  type="button"
                  className="platform-btn"
                  onClick={() => handleAdd(platform)}
                  style={{ borderColor: platformColors[platform] }}
                >
                  <img src={platformIcons[platform]} alt="" className="platform-btn-icon" />
                  <span>{platformLabels[platform]}</span>
                </button>
              ))}
            </div>
          </div>
        )}
      </div>
    </section>
  );
}
import { useState } from 'react';
import type { MobileApp } from '../types/brand';

interface MobileAppsProps {
  apps: MobileApp[];
  onUpdate: (apps: MobileApp[]) => void;
}

export function MobileApps({ apps, onUpdate }: MobileAppsProps) {
  const [editingId, setEditingId] = useState<string | null>(null);
  const [editForm, setEditForm] = useState<Partial<MobileApp>>({});
  const [logoPreview, setLogoPreview] = useState<string | null>(null);

  const handleAdd = () => {
    const newApp: MobileApp = {
      id: `app-${Date.now()}`,
      name: '',
      packageId: '',
      developer: '',
      storeUrl: '',
      logo: '',
      description: '',
    };
    onUpdate([...apps, newApp]);
    setEditingId(newApp.id);
    setEditForm({ ...newApp });
    setLogoPreview(null);
  };

  const handleEdit = (app: MobileApp) => {
    setEditingId(app.id);
    setEditForm({ ...app });
    setLogoPreview(app.logo);
  };

  const handleSave = (id: string) => {
    const updated = apps.map((a) => (a.id === id ? { ...a, ...editForm } : a));
    onUpdate(updated);
    setEditingId(null);
    setEditForm({});
    setLogoPreview(null);
  };

  const handleCancel = () => {
    setEditingId(null);
    setEditForm({});
    setLogoPreview(null);
  };

  const handleRemove = (id: string) => {
    onUpdate(apps.filter((a) => a.id !== id));
  };

  const handleChange = (field: keyof MobileApp, value: string) => {
    setEditForm({ ...editForm, [field]: value });
  };

  const handleLogoUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (event) => {
        const result = event.target?.result as string;
        setLogoPreview(result);
        handleChange('logo', result);
      };
      reader.readAsDataURL(file);
    }
  };

  return (
    <section className="section-card" aria-labelledby="mobile-apps-heading">
      <div className="section-header">
        <h2 id="mobile-apps-heading" className="section-title">
          <svg className="section-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <rect x="5" y="2" width="14" height="20" rx="2" ry="2" />
            <path d="M12 18h.01" />
          </svg>
          Official Mobile Apps
        </h2>
        <span className="badge badge-trusted">TRUSTED OFFICIAL</span>
      </div>

      <div className="mobile-apps-container">
        {apps.length > 0 ? (
          <div className="apps-grid">
            {apps.map((app) => (
              <article key={app.id} className={`app-card ${editingId === app.id ? 'editing' : ''}`}>
                {editingId === app.id ? (
                  <div className="app-edit-form">
                    <div className="app-logo-upload">
                      <label className="logo-upload-small">
                        <div
                          className="logo-preview-small"
                          style={{ backgroundImage: `url(${logoPreview || app.logo || 'https://via.placeholder.com/80/ccc/fff?text=App'})` }}
                        />
                        <input
                          type="file"
                          accept="image/*"
                           onChange={(e) => handleLogoUpload(e)}
                          className="file-input"
                        />
                        <span className="upload-overlay-small">Change</span>
                      </label>
                    </div>

                    <div className="edit-fields">
                      <div className="form-group">
                        <label htmlFor={`app-name-${app.id}`} className="form-label">App Name *</label>
                        <input
                          id={`app-name-${app.id}`}
                          type="text"
                          className="form-input"
                          value={editForm.name || ''}
                          onChange={(e) => handleChange('name', e.target.value)}
                          placeholder="e.g., SecureBank Mobile"
                        />
                      </div>

                      <div className="form-group">
                        <label htmlFor={`package-id-${app.id}`} className="form-label">Package ID / App ID *</label>
                        <input
                          id={`package-id-${app.id}`}
                          type="text"
                          className="form-input"
                          value={editForm.packageId || ''}
                          onChange={(e) => handleChange('packageId', e.target.value)}
                          placeholder="com.securebank.mobile"
                        />
                      </div>

                      <div className="form-group">
                        <label htmlFor={`developer-${app.id}`} className="form-label">Official Developer / Publisher *</label>
                        <input
                          id={`developer-${app.id}`}
                          type="text"
                          className="form-input"
                          value={editForm.developer || ''}
                          onChange={(e) => handleChange('developer', e.target.value)}
                          placeholder="SecureBank Financial Services Inc."
                        />
                      </div>

                      <div className="form-group">
                        <label htmlFor={`store-url-${app.id}`} className="form-label">App Store URL *</label>
                        <input
                          id={`store-url-${app.id}`}
                          type="url"
                          className="form-input"
                          value={editForm.storeUrl || ''}
                          onChange={(e) => handleChange('storeUrl', e.target.value)}
                          placeholder="https://play.google.com/store/apps/details?id=..."
                        />
                      </div>

                      <div className="form-group">
                        <label htmlFor={`description-${app.id}`} className="form-label">App Description</label>
                        <textarea
                          id={`description-${app.id}`}
                          className="form-textarea"
                          value={editForm.description || ''}
                          onChange={(e) => handleChange('description', e.target.value)}
                          placeholder="Describe the app..."
                          rows={2}
                        />
                      </div>

                      <div className="edit-actions">
                        <button type="button" className="btn btn-primary btn-sm" onClick={() => handleSave(app.id)}>
                          Save
                        </button>
                        <button type="button" className="btn btn-secondary btn-sm" onClick={handleCancel}>
                          Cancel
                        </button>
                      </div>
                    </div>
                  </div>
                ) : (
                  <div className="app-view">
                    <div className="app-header">
                      <div
                        className="app-logo"
                        style={{ backgroundImage: `url(${app.logo || 'https://via.placeholder.com/80/ccc/fff?text=App'})` }}
                      />
                      <div className="app-meta">
                        <h3 className="app-name">{app.name || 'Unnamed App'}</h3>
                        <span className="app-package">{app.packageId || 'No package ID'}</span>
                      </div>
                    </div>

                    <div className="app-details">
                      <div className="detail-row">
                        <span className="detail-label">Developer:</span>
                        <span className="detail-value">{app.developer || 'Not set'}</span>
                      </div>
                      <div className="detail-row">
                        <span className="detail-label">Store:</span>
                        <a href={app.storeUrl} target="_blank" rel="noopener noreferrer" className="store-link">
                          View on Store
                          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className="external-icon">
                            <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6" />
                            <polyline points="15 3 21 3 21 9" />
                            <line x1="10" y1="14" x2="21" y2="3" />
                          </svg>
                        </a>
                      </div>
                    </div>

                    {app.description && (
                      <p className="app-description">{app.description}</p>
                    )}

                    <div className="app-actions">
                      <button
                        type="button"
                        className="btn btn-secondary btn-sm"
                        onClick={() => handleEdit(app)}
                      >
                        Edit
                      </button>
                      <button
                        type="button"
                        className="btn btn-danger btn-sm"
                        onClick={() => handleRemove(app.id)}
                      >
                        Remove
                      </button>
                    </div>
                  </div>
                )}
              </article>
            ))}
          </div>
        ) : (
          <div className="empty-state">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" className="empty-icon">
              <rect x="5" y="2" width="14" height="20" rx="2" ry="2" />
              <path d="M12 18h.01" />
            </svg>
            <h3>No Official Mobile Apps Registered</h3>
            <p>Add your brand's official mobile applications to establish the trusted baseline.</p>
          </div>
        )}

        <button type="button" className="btn btn-primary add-app-btn" onClick={handleAdd}>
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className="btn-icon">
            <line x1="12" y1="5" x2="12" y2="19" />
            <line x1="5" y1="12" x2="19" y2="12" />
          </svg>
          Add Official App
        </button>
      </div>
    </section>
  );
}
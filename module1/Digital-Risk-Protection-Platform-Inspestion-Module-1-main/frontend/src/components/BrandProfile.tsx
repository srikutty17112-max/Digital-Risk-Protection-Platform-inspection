import { useState } from 'react';
import type { BrandProfile } from '../types/brand';

interface BrandProfileProps {
  brand: BrandProfile;
  onUpdate: (brand: BrandProfile) => void;
  onLogoChange: (logoUrl: string) => void;
}

const defaultKeywords = ['banking', 'fintech', 'digital banking', 'secure payments', 'financial services'];
const defaultAliases = ['Secure Bank', 'SecureBank Financial', 'SBFS'];

export function BrandProfile({ brand, onUpdate, onLogoChange }: BrandProfileProps) {
  const [logoUrl, setLogoUrl] = useState(brand.logo);
  const [logoPreview, setLogoPreview] = useState<string | null>(null);
  const [keywords, setKeywords] = useState<string[]>(brand.keywords.length ? brand.keywords : defaultKeywords);
  const [aliases, setAliases] = useState<string[]>(brand.aliases.length ? brand.aliases : defaultAliases);
  const [newKeyword, setNewKeyword] = useState('');
  const [newAlias, setNewAlias] = useState('');

  const handleLogoUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (event) => {
        const result = event.target?.result as string;
        setLogoPreview(result);
        setLogoUrl(result);
        onLogoChange(result);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleKeywordAdd = () => {
    if (newKeyword.trim() && !keywords.includes(newKeyword.trim())) {
      setKeywords([...keywords, newKeyword.trim()]);
      setNewKeyword('');
    }
  };

  const handleAliasAdd = () => {
    if (newAlias.trim() && !aliases.includes(newAlias.trim())) {
      setAliases([...aliases, newAlias.trim()]);
      setNewAlias('');
    }
  };

  const handleKeywordRemove = (keyword: string) => {
    setKeywords(keywords.filter((k) => k !== keyword));
  };

  const handleAliasRemove = (alias: string) => {
    setAliases(aliases.filter((a) => a !== alias));
  };

  const handleSubmit = () => {
    const updatedBrand: BrandProfile = {
      ...brand,
      keywords,
      aliases,
      logo: logoUrl,
    };
    onUpdate(updatedBrand);
  };

  return (
    <section className="section-card" aria-labelledby="brand-profile-heading">
      <div className="section-header">
        <h2 id="brand-profile-heading" className="section-title">
          <svg className="section-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M12 2L2 7l10 5 10-5-10-5z" />
            <path d="M2 17l10 5 10-5" />
            <path d="M2 12l10 5 10-5" />
          </svg>
          Brand Profile
        </h2>
        <span className="badge badge-trusted">TRUSTED OFFICIAL</span>
      </div>

      <div className="brand-profile-grid">
        <div className="logo-section">
          <label className="logo-upload">
            <div className="logo-preview" style={{ backgroundImage: `url(${logoPreview || logoUrl})` }} />
            <input type="file" accept="image/*" onChange={handleLogoUpload} className="file-input" />
            <span className="upload-overlay">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className="upload-icon">
                <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
                <polyline points="17 8 12 3 7 8" />
                <line x1="12" y1="3" x2="12" y2="15" />
              </svg>
              Upload Logo
            </span>
          </label>
          <p className="logo-hint">Official brand logo (PNG, JPG, SVG)</p>
        </div>

        <div className="form-section">
          <div className="form-row">
            <div className="form-group">
              <label htmlFor="brandName" className="form-label">Brand Name *</label>
              <input
                id="brandName"
                type="text"
                className="form-input"
                value={brand.brandName}
                onChange={(e) => onUpdate({ ...brand, brandName: e.target.value })}
                placeholder="e.g., SecureBank"
              />
            </div>
            <div className="form-group">
              <label htmlFor="companyName" className="form-label">Company Name *</label>
              <input
                id="companyName"
                type="text"
                className="form-input"
                value={brand.companyName}
                onChange={(e) => onUpdate({ ...brand, companyName: e.target.value })}
                placeholder="e.g., SecureBank Financial Services Inc."
              />
            </div>
          </div>

          <div className="form-group">
            <label htmlFor="officialWebsite" className="form-label">Official Website *</label>
            <input
              id="officialWebsite"
              type="url"
              className="form-input"
              value={brand.officialWebsite}
              onChange={(e) => onUpdate({ ...brand, officialWebsite: e.target.value })}
              placeholder="https://securebank.com"
            />
          </div>

          <div className="form-group">
            <label htmlFor="description" className="form-label">Brand Description</label>
            <textarea
              id="description"
              className="form-textarea"
              value={brand.description}
              onChange={(e) => onUpdate({ ...brand, description: e.target.value })}
              placeholder="Describe your brand..."
              rows={3}
            />
          </div>

          <div className="form-group">
            <label className="form-label">Brand Keywords / Aliases</label>
            <div className="tag-input">
              <div className="tag-list">
                {keywords.map((keyword) => (
                  <span key={keyword} className="tag tag-keyword">
                    {keyword}
                    <button type="button" className="tag-remove" onClick={() => handleKeywordRemove(keyword)} aria-label={`Remove ${keyword}`}>
                      ×
                    </button>
                  </span>
                ))}
              </div>
              <div className="tag-input-row">
                <input
                  type="text"
                  className="form-input tag-input-field"
                  value={newKeyword}
                  onChange={(e) => setNewKeyword(e.target.value)}
                  onKeyDown={(e) => e.key === 'Enter' && (e.preventDefault(), handleKeywordAdd())}
                  placeholder="Add keyword..."
                />
                <button type="button" className="btn btn-secondary btn-sm" onClick={handleKeywordAdd}>
                  Add
                </button>
              </div>
            </div>
          </div>

          <div className="form-group">
            <label className="form-label">Brand Aliases</label>
            <div className="tag-input">
              <div className="tag-list">
                {aliases.map((alias) => (
                  <span key={alias} className="tag tag-alias">
                    {alias}
                    <button type="button" className="tag-remove" onClick={() => handleAliasRemove(alias)} aria-label={`Remove ${alias}`}>
                      ×
                    </button>
                  </span>
                ))}
              </div>
              <div className="tag-input-row">
                <input
                  type="text"
                  className="form-input tag-input-field"
                  value={newAlias}
                  onChange={(e) => setNewAlias(e.target.value)}
                  onKeyDown={(e) => e.key === 'Enter' && (e.preventDefault(), handleAliasAdd())}
                  placeholder="Add alias..."
                />
                <button type="button" className="btn btn-secondary btn-sm" onClick={handleAliasAdd}>
                  Add
                </button>
              </div>
            </div>
          </div>

          <div className="form-actions">
            <button type="button" className="btn btn-primary" onClick={handleSubmit}>
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className="btn-icon">
                <path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z" />
                <polyline points="17 21 17 13 7 13 7 21" />
                <polyline points="7 3 7 8 15 8" />
              </svg>
              Save Brand Profile
            </button>
          </div>
        </div>
      </div>
    </section>
  );
}
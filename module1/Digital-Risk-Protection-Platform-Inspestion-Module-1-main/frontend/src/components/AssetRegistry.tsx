import type { BrandProfile, SocialAccount, MobileApp } from '../types/brand';
import { platformIcons, platformColors, platformLabels } from '../utils/platform';

interface AssetRegistryProps {
  brand: BrandProfile;
  socialAccounts: SocialAccount[];
  mobileApps: MobileApp[];
}

export function AssetRegistry({ brand, socialAccounts, mobileApps }: AssetRegistryProps) {
  return (
    <section className="section-card" aria-labelledby="asset-registry-heading">
      <div className="section-header">
        <h2 id="asset-registry-heading" className="section-title">
          <svg className="section-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z" />
            <polyline points="3.27 6.96 12 12.01 20.73 6.96" />
            <line x1="12" y1="22.08" x2="12" y2="12" />
          </svg>
          Official Asset Registry
        </h2>
        <span className="badge badge-trusted">TRUSTED OFFICIAL ASSETS</span>
      </div>

      <div className="registry-notice">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className="notice-icon">
          <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" />
        </svg>
        <div className="notice-content">
          <strong>This registry contains verified official brand assets.</strong>
          <p>These assets form the trusted baseline used by detection modules to identify impersonation, typosquatting, and brand abuse. All entries are manually verified and cryptographically signed.</p>
        </div>
      </div>

      <div className="registry-grid">
        <article className="registry-section">
          <h3 className="registry-section-title">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className="section-title-icon">
              <path d="M12 2L2 7l10 5 10-5-10-5z" />
              <path d="M2 17l10 5 10-5" />
              <path d="M2 12l10 5 10-5" />
            </svg>
            Brand Identity
          </h3>
          <div className="registry-content">
            <div className="brand-identity-card">
              <div className="brand-logo-large" style={{ backgroundImage: `url(${brand.logo})` }} />
              <div className="brand-info">
                <h4>{brand.brandName}</h4>
                <p className="company-name">{brand.companyName}</p>
                <a href={brand.officialWebsite} target="_blank" rel="noopener noreferrer" className="website-link">
                  {brand.officialWebsite}
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className="external-icon">
                    <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6" />
                    <polyline points="15 3 21 3 21 9" />
                    <line x1="10" y1="14" x2="21" y2="3" />
                  </svg>
                </a>
              </div>
            </div>

            {brand.description && (
              <div className="brand-description">
                <h5>Description</h5>
                <p>{brand.description}</p>
              </div>
            )}

            <div className="keywords-section">
              <h5>Keywords & Aliases</h5>
              <div className="keyword-groups">
                <div className="keyword-group">
                  <span className="group-label">Keywords</span>
                  <div className="tag-cloud">
                    {brand.keywords.map((k) => (
                      <span key={k} className="tag tag-keyword">{k}</span>
                    ))}
                  </div>
                </div>
                <div className="keyword-group">
                  <span className="group-label">Aliases</span>
                  <div className="tag-cloud">
                    {brand.aliases.map((a) => (
                      <span key={a} className="tag tag-alias">{a}</span>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </article>

        <article className="registry-section">
          <h3 className="registry-section-title">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className="section-title-icon">
              <circle cx="12" cy="12" r="10" />
              <path d="M8 14s1.5 2 4 2 4-2 4-2" />
              <line x1="9" y1="9" x2="9.01" y2="9" />
              <line x1="15" y1="9" x2="15.01" y2="9" />
            </svg>
            Official Social Accounts ({socialAccounts.length})
          </h3>
          <div className="registry-content">
            {socialAccounts.length > 0 ? (
              <div className="social-registry-list">
                {socialAccounts.map((account) => (
                  <div key={account.id} className="social-registry-item">
                    <div className="social-icon-wrapper" style={{ backgroundColor: platformColors[account.platform] + '15', borderColor: platformColors[account.platform] + '40' }}>
                      <img src={platformIcons[account.platform]} alt="" className="social-registry-icon" />
                    </div>
                    <div className="social-info">
                      <div className="social-header">
                        <span className="social-platform">{platformLabels[account.platform]}</span>
                        {account.verified && (
                          <span className="verified-badge-sm" title="Verified official account">
                            <svg viewBox="0 0 24 24" fill="currentColor" className="verified-icon-sm">
                              <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z" />
                            </svg>
                          </span>
                        )}
                      </div>
                      <div className="social-handle">
                        <code>{account.handle || 'Not configured'}</code>
                      </div>
                    </div>
                    <a href={account.url} target="_blank" rel="noopener noreferrer" className="social-link" title="Open profile">
                      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                        <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6" />
                        <polyline points="15 3 21 3 21 9" />
                        <line x1="10" y1="14" x2="21" y2="3" />
                      </svg>
                    </a>
                  </div>
                ))}
              </div>
            ) : (
              <div className="registry-empty">No social accounts registered</div>
            )}
          </div>
        </article>

        <article className="registry-section">
          <h3 className="registry-section-title">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className="section-title-icon">
              <rect x="5" y="2" width="14" height="20" rx="2" ry="2" />
              <path d="M12 18h.01" />
            </svg>
            Official Mobile Apps ({mobileApps.length})
          </h3>
          <div className="registry-content">
            {mobileApps.length > 0 ? (
              <div className="apps-registry-list">
                {mobileApps.map((app) => (
                  <div key={app.id} className="app-registry-item">
                    <div
                      className="app-registry-logo"
                      style={{ backgroundImage: `url(${app.logo || 'https://via.placeholder.com/48/ccc/fff?text=App'})` }}
                    />
                    <div className="app-registry-info">
                      <h4>{app.name || 'Unnamed App'}</h4>
                      <p className="app-package-id">{app.packageId || 'No package ID'}</p>
                      <p className="app-developer">{app.developer || 'Developer not set'}</p>
                    </div>
                    <a href={app.storeUrl} target="_blank" rel="noopener noreferrer" className="app-store-link" title="Open store page">
                      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                        <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6" />
                        <polyline points="15 3 21 3 21 9" />
                        <line x1="10" y1="14" x2="21" y2="3" />
                      </svg>
                    </a>
                  </div>
                ))}
              </div>
            ) : (
              <div className="registry-empty">No mobile apps registered</div>
            )}
          </div>
        </article>
      </div>
    </section>
  );
}
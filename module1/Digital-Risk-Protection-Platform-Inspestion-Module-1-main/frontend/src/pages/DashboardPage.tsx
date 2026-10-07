import { BrandProfile } from '../components/BrandProfile';
import { AssetRegistry } from '../components/AssetRegistry';
import { BrandFingerprint } from '../components/BrandFingerprint';
import type { BrandProfile as BrandProfileType } from '../types/brand';
import { demoBrand, demoSocialAccounts, demoMobileApps, demoBrandFingerprint } from '../data/demoData';
import type { BrandFingerprint as BrandFingerprintType } from '../types/brand';
import { useState } from 'react';

export function DashboardPage() {
  const [brand, setBrand] = useState<BrandProfileType>(demoBrand);
  const socialAccounts = demoSocialAccounts;
  const mobileApps = demoMobileApps;
  const [fingerprint] = useState<BrandFingerprintType>(demoBrandFingerprint);

  return (
    <div className="page">
      <div className="page-header">
        <h1>Dashboard</h1>
        <p>Brand Intelligence Platform — Module 1: Brand Baseline & Official Asset Registry</p>
      </div>

      <div className="stats-grid">
        <article className="stat-card">
          <div className="stat-icon brand">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M12 2L2 7l10 5 10-5-10-5z" />
              <path d="M2 17l10 5 10-5" />
              <path d="M2 12l10 5 10-5" />
            </svg>
          </div>
          <div className="stat-info">
            <span className="stat-value">1</span>
            <span className="stat-label">Brand Profile</span>
          </div>
        </article>

        <article className="stat-card">
          <div className="stat-icon social">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <circle cx="12" cy="12" r="10" />
              <path d="M8 14s1.5 2 4 2 4-2 4-2" />
              <line x1="9" y1="9" x2="9.01" y2="9" />
              <line x1="15" y1="9" x2="15.01" y2="9" />
            </svg>
          </div>
          <div className="stat-info">
            <span className="stat-value">{socialAccounts.filter(a => a.verified).length}</span>
            <span className="stat-label">Verified Social Accounts</span>
          </div>
        </article>

        <article className="stat-card">
          <div className="stat-icon apps">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <rect x="5" y="2" width="14" height="20" rx="2" ry="2" />
              <path d="M12 18h.01" />
            </svg>
          </div>
          <div className="stat-info">
            <span className="stat-value">{mobileApps.length}</span>
            <span className="stat-label">Official Mobile Apps</span>
          </div>
        </article>

        <article className="stat-card">
          <div className="stat-icon fingerprint">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" />
              <circle cx="12" cy="7" r="4" />
            </svg>
          </div>
          <div className="stat-info">
            <span className="stat-value">{fingerprint.similarityScore}%</span>
            <span className="stat-label">Baseline Similarity</span>
          </div>
        </article>
      </div>

      <div className="dashboard-grid">
        <section className="section-card dashboard-section" aria-labelledby="quick-actions-heading">
          <h2 id="quick-actions-heading" className="section-title">
            <svg className="section-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <polyline points="16 18 22 12 16 6" />
              <polyline points="8 6 2 12 8 18" />
            </svg>
            Quick Actions
          </h2>
          <div className="action-buttons-grid">
            <a href="/brand-profile" className="action-btn primary">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className="action-icon">
                <path d="M12 2L2 7l10 5 10-5-10-5z" />
                <path d="M2 17l10 5 10-5" />
                <path d="M2 12l10 5 10-5" />
              </svg>
              <div className="action-content">
                <span className="action-label">Configure Brand Profile</span>
                <span className="action-desc">Set up brand identity, logo, keywords & aliases</span>
              </div>
            </a>
            <a href="/social-accounts" className="action-btn secondary">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className="action-icon">
                <circle cx="12" cy="12" r="10" />
                <path d="M8 14s1.5 2 4 2 4-2 4-2" />
                <line x1="9" y1="9" x2="9.01" y2="9" />
                <line x1="15" y1="9" x2="15.01" y2="9" />
              </svg>
              <div className="action-content">
                <span className="action-label">Manage Social Accounts</span>
                <span className="action-desc">Register official social media profiles</span>
              </div>
            </a>
            <a href="/mobile-apps" className="action-btn secondary">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className="action-icon">
                <rect x="5" y="2" width="14" height="20" rx="2" ry="2" />
                <path d="M12 18h.01" />
              </svg>
              <div className="action-content">
                <span className="action-label">Register Mobile Apps</span>
                <span className="action-desc">Add official iOS & Android applications</span>
              </div>
            </a>
            <a href="/asset-registry" className="action-btn secondary">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className="action-icon">
                <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z" />
                <polyline points="3.27 6.96 12 12.01 20.73 6.96" />
                <line x1="12" y1="22.08" x2="12" y2="12" />
              </svg>
              <div className="action-content">
                <span className="action-label">View Asset Registry</span>
                <span className="action-desc">Review all trusted official assets</span>
              </div>
            </a>
          </div>
        </section>

        <section className="section-card dashboard-section" aria-labelledby="brand-summary-heading">
          <h2 id="brand-summary-heading" className="section-title">
            <svg className="section-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <circle cx="12" cy="12" r="10" />
              <path d="M12 6v6l4 2" />
            </svg>
            Brand Summary
          </h2>
          <div className="brand-summary">
            <div className="summary-logo" style={{ backgroundImage: `url(${brand.logo})` }} />
            <div className="summary-info">
              <h3>{brand.brandName}</h3>
              <p className="summary-company">{brand.companyName}</p>
              <a href={brand.officialWebsite} target="_blank" rel="noopener noreferrer" className="summary-website">
                {brand.officialWebsite}
              </a>
            </div>
            <div className="summary-meta">
              <div className="meta-item">
                <span className="meta-label">Keywords</span>
                <span className="meta-value">{brand.keywords.length}</span>
              </div>
              <div className="meta-item">
                <span className="meta-label">Aliases</span>
                <span className="meta-value">{brand.aliases.length}</span>
              </div>
              <div className="meta-item">
                <span className="meta-label">Social Accounts</span>
                <span className="meta-value">{socialAccounts.length}</span>
              </div>
              <div className="meta-item">
                <span className="meta-label">Mobile Apps</span>
                <span className="meta-value">{mobileApps.length}</span>
              </div>
            </div>
          </div>
        </section>
      </div>

      <BrandProfile brand={brand} onUpdate={setBrand} onLogoChange={() => {}} />
      <AssetRegistry brand={brand} socialAccounts={socialAccounts} mobileApps={mobileApps} />
      <BrandFingerprint fingerprint={fingerprint} />
    </div>
  );
}
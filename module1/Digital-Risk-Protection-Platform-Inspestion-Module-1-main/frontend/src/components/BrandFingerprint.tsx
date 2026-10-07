import type { BrandFingerprint } from '../types/brand';

interface BrandFingerprintProps {
  fingerprint: BrandFingerprint;
}

export function BrandFingerprint({ fingerprint }: BrandFingerprintProps) {
  const getScoreColor = (score: number) => {
    if (score >= 90) return 'score-high';
    if (score >= 70) return 'score-medium';
    return 'score-low';
  };

  const getScoreLabel = (score: number) => {
    if (score >= 90) return 'Exact Match';
    if (score >= 70) return 'High Similarity';
    if (score >= 50) return 'Moderate Similarity';
    return 'Low Similarity';
  };

  return (
    <section className="section-card fingerprint-section" aria-labelledby="fingerprint-heading">
      <div className="section-header">
        <h2 id="fingerprint-heading" className="section-title">
          <svg className="section-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" />
            <circle cx="12" cy="7" r="4" />
          </svg>
          Brand Fingerprint
        </h2>
        <span className="badge badge-fingerprint">COMPARISON BASELINE</span>
      </div>

      <div className="fingerprint-notice">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className="notice-icon">
          <circle cx="12" cy="12" r="10" />
          <path d="M12 16v-4" />
          <path d="M12 8h.01" />
        </svg>
        <div className="notice-content">
          <strong>This fingerprint serves as the comparison baseline for detection modules.</strong>
          <p>The normalized brand identity flows through the similarity engine to generate similarity scores against candidate names. This baseline is consumed by Module 2+ for threat detection, impersonation identification, and typosquatting analysis.</p>
        </div>
      </div>

      <div className="fingerprint-flow">
        <div className="flow-step">
          <div className="step-card">
            <div className="step-number">1</div>
            <div className="step-label">Official Brand Name</div>
            <div className="step-value">{fingerprint.officialBrandName}</div>
          </div>
        </div>

        <div className="flow-arrow">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M5 12h14" />
            <path d="M12 5l7 7-7 7" />
          </svg>
        </div>

        <div className="flow-step">
          <div className="step-card">
            <div className="step-number">2</div>
            <div className="step-label">Normalization</div>
            <div className="step-value normalized">{fingerprint.normalizedName}</div>
          </div>
        </div>

        <div className="flow-arrow">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M5 12h14" />
            <path d="M12 5l7 7-7 7" />
          </svg>
        </div>

        <div className="flow-step">
          <div className="step-card engine-card">
            <div className="step-number">3</div>
            <div className="step-label">Similarity Engine</div>
            <div className="step-value engine-name">{fingerprint.similarityEngine}</div>
          </div>
        </div>

        <div className="flow-arrow">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M5 12h14" />
            <path d="M12 5l7 7-7 7" />
          </svg>
        </div>

        <div className="flow-step">
          <div className="step-card">
            <div className="step-number">4</div>
            <div className="step-label">Candidate Name</div>
            <div className="step-value candidate">{fingerprint.candidateName}</div>
          </div>
        </div>

        <div className="flow-arrow">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M5 12h14" />
            <path d="M12 5l7 7-7 7" />
          </svg>
        </div>

        <div className="flow-step">
          <div className="step-card score-card">
            <div className="step-number">5</div>
            <div className="step-label">Similarity Score</div>
            <div className={`step-value score-display ${getScoreColor(fingerprint.similarityScore)}`}>
              <span className="score-number">{fingerprint.similarityScore}%</span>
              <span className="score-label">{getScoreLabel(fingerprint.similarityScore)}</span>
            </div>
            <div className="score-bar">
              <div
                className="score-fill"
                style={{ width: `${fingerprint.similarityScore}%` }}
              />
            </div>
          </div>
        </div>
      </div>

      <div className="fingerprint-meta">
        <h4>Data Export Structure</h4>
        <pre className="json-preview">{JSON.stringify(
          {
            brand: fingerprint.officialBrandName,
            normalized: fingerprint.normalizedName,
            engine: fingerprint.similarityEngine,
            candidate: fingerprint.candidateName,
            score: fingerprint.similarityScore,
            baseline: true,
            purpose: 'Module 1 official brand fingerprint for cross-module comparison',
          },
          null,
          2
        )}</pre>
      </div>
    </section>
  );
}
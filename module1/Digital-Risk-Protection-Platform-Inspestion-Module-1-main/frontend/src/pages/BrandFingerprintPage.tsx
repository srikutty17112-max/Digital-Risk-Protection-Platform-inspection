import { BrandFingerprint } from '../components/BrandFingerprint';
import { demoBrandFingerprint } from '../data/demoData';

export function BrandFingerprintPage() {
  return (
    <div className="page">
      <div className="page-header">
        <h1>Brand Fingerprint</h1>
        <p>Visual representation of the official brand fingerprint used as comparison baseline for threat detection modules</p>
      </div>

      <BrandFingerprint fingerprint={demoBrandFingerprint} />
    </div>
  );
}
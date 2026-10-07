import { AssetRegistry } from '../components/AssetRegistry';
import { demoBrand, demoSocialAccounts, demoMobileApps } from '../data/demoData';

export function AssetRegistryPage() {
  return (
    <div className="page">
      <div className="page-header">
        <h1>Official Asset Registry</h1>
        <p>Complete view of all trusted official brand assets — this registry serves as the comparison baseline for detection modules</p>
      </div>

      <AssetRegistry brand={demoBrand} socialAccounts={demoSocialAccounts} mobileApps={demoMobileApps} />
    </div>
  );
}
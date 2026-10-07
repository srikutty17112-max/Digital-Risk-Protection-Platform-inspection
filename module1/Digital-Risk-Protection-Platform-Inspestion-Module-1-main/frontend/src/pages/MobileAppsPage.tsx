import { MobileApps } from '../components/MobileApps';
import type { MobileApp } from '../types/brand';
import { demoMobileApps } from '../data/demoData';
import { useState } from 'react';

export function MobileAppsPage() {
  const [apps, setApps] = useState<MobileApp[]>(demoMobileApps);

  return (
    <div className="page">
      <div className="page-header">
        <h1>Official Mobile Apps</h1>
        <p>Register and manage your brand's official iOS and Android applications</p>
      </div>

      <MobileApps apps={apps} onUpdate={setApps} />
    </div>
  );
}
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { Layout } from './components/Layout';
import { DashboardPage } from './pages/DashboardPage';
import { BrandProfilePage } from './pages/BrandProfilePage';
import { SocialAccountsPage } from './pages/SocialAccountsPage';
import { MobileAppsPage } from './pages/MobileAppsPage';
import { AssetRegistryPage } from './pages/AssetRegistryPage';
import { BrandFingerprintPage } from './pages/BrandFingerprintPage';
import './App.css';

function App() {
  return (
    <BrowserRouter>
      <Layout>
        <Routes>
          <Route path="/" element={<DashboardPage />} />
          <Route path="/brand-profile" element={<BrandProfilePage />} />
          <Route path="/social-accounts" element={<SocialAccountsPage />} />
          <Route path="/mobile-apps" element={<MobileAppsPage />} />
          <Route path="/asset-registry" element={<AssetRegistryPage />} />
          <Route path="/brand-fingerprint" element={<BrandFingerprintPage />} />
        </Routes>
      </Layout>
    </BrowserRouter>
  );
}

export default App;
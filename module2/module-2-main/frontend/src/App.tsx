import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import ScansPage from './pages/ScansPage';
import ThreatsPage from './pages/ThreatsPage';
import CandidatesPage from './pages/CandidatesPage';
import DashboardPage from './pages/DashboardPage';
import DetectionsPage from './pages/DetectionsPage';
import AccountsPage from './pages/AccountsPage';

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<ScansPage />} />
          <Route path="scans" element={<ScansPage />} />
          <Route path="threats" element={<ThreatsPage />} />
          <Route path="candidates" element={<CandidatesPage />} />
          <Route path="dashboard" element={<DashboardPage />} />
          <Route path="detections" element={<DetectionsPage />} />
          <Route path="accounts" element={<AccountsPage />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

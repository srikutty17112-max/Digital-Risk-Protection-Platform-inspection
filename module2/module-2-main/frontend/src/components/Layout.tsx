import { Link, Outlet } from 'react-router-dom';

export default function Layout() {
  return (
    <div className="app">
      <header className="header">
        <h1>BrandShield</h1>
        <nav>
          <Link to="/dashboard">Dashboard</Link>
          <Link to="/detections">Detections</Link>
          <Link to="/accounts">Accounts</Link>
          <Link to="/scans">Scans</Link>
          <Link to="/threats">Threats</Link>
          <Link to="/candidates">Candidates</Link>
        </nav>
      </header>
      <main className="main">
        <Outlet />
      </main>
    </div>
  );
}

import { Sidebar } from './Sidebar';
import { type ReactNode, useState } from 'react';

interface LayoutProps {
  children?: ReactNode;
}

export function Layout({ children }: LayoutProps) {
  const [sidebarOpen, setSidebarOpen] = useState(false);

  return (
    <div className="layout">
      <Sidebar isOpen={sidebarOpen} onClose={() => setSidebarOpen(false)} />

      <main className="main-content" role="main">
        <header className="top-bar">
          <button
            className="mobile-menu-btn"
            onClick={() => setSidebarOpen(true)}
            aria-label="Open navigation menu"
          >
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <line x1="3" y1="12" x2="21" y2="12" />
              <line x1="3" y1="6" x2="21" y2="6" />
              <line x1="3" y1="18" x2="21" y2="18" />
            </svg>
          </button>

          <div className="page-header">
            <h1 className="page-title">Brand Intelligence Platform</h1>
            <p className="page-subtitle">Module 1 — Brand Baseline & Official Asset Registry</p>
          </div>

          <div className="top-bar-actions">
            <span className="status-indicator">
              <span className="status-dot online" />
              <span>Live</span>
            </span>
          </div>
        </header>

        <div className="content-wrapper">
          {children}
        </div>
      </main>
    </div>
  );
}
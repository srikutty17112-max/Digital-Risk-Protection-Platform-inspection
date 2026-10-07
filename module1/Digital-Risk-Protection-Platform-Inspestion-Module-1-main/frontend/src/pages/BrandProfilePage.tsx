import { BrandProfile } from '../components/BrandProfile';
import type { BrandProfile as BrandProfileType } from '../types/brand';
import { demoBrand } from '../data/demoData';
import { useState } from 'react';

export function BrandProfilePage() {
  const [brand, setBrand] = useState<BrandProfileType>(demoBrand);

  return (
    <div className="page">
      <div className="page-header">
        <h1>Brand Profile</h1>
        <p>Configure the official brand identity, logo, keywords, and aliases</p>
      </div>

      <BrandProfile brand={brand} onUpdate={setBrand} onLogoChange={() => {}} />
    </div>
  );
}
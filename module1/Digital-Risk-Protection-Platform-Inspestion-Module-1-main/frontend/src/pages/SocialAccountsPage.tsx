import { SocialAccounts } from '../components/SocialAccounts';
import type { SocialAccount } from '../types/brand';
import { demoSocialAccounts } from '../data/demoData';
import { useState } from 'react';

export function SocialAccountsPage() {
  const [accounts, setAccounts] = useState<SocialAccount[]>(demoSocialAccounts);

  return (
    <div className="page">
      <div className="page-header">
        <h1>Official Social Accounts</h1>
        <p>Register and manage your brand's verified social media profiles</p>
      </div>

      <SocialAccounts accounts={accounts} onUpdate={setAccounts} />
    </div>
  );
}
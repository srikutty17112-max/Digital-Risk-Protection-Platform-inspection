import type { BrandProfile, SocialAccount, MobileApp, BrandFingerprint } from '../types/brand';

export const demoBrand: BrandProfile = {
  id: 'brand-1',
  brandName: 'SecureBank',
  companyName: 'SecureBank Financial Services Inc.',
  officialWebsite: 'https://securebank.com',
  description: 'SecureBank is a leading digital banking platform providing secure financial services to millions of customers worldwide. Founded in 2010, we pioneered zero-trust architecture in consumer banking.',
  keywords: ['banking', 'fintech', 'digital banking', 'secure payments', 'financial services'],
  aliases: ['Secure Bank', 'SecureBank Financial', 'SBFS'],
  logo: 'https://via.placeholder.com/120x120/1a56db/ffffff?text=SB',
};

export const demoSocialAccounts: SocialAccount[] = [
  {
    id: 'social-1',
    platform: 'twitter',
    url: 'https://twitter.com/securebank',
    handle: '@securebank',
    verified: true,
  },
  {
    id: 'social-2',
    platform: 'linkedin',
    url: 'https://linkedin.com/company/securebank',
    handle: 'securebank',
    verified: true,
  },
  {
    id: 'social-3',
    platform: 'facebook',
    url: 'https://facebook.com/securebank',
    handle: 'securebank',
    verified: true,
  },
  {
    id: 'social-4',
    platform: 'instagram',
    url: 'https://instagram.com/securebank',
    handle: '@securebank',
    verified: true,
  },
  {
    id: 'social-5',
    platform: 'youtube',
    url: 'https://youtube.com/@securebank',
    handle: '@securebank',
    verified: true,
  },
];

export const demoMobileApps: MobileApp[] = [
  {
    id: 'app-1',
    name: 'SecureBank Mobile',
    packageId: 'com.securebank.mobile',
    developer: 'SecureBank Financial Services Inc.',
    storeUrl: 'https://play.google.com/store/apps/details?id=com.securebank.mobile',
    logo: 'https://via.placeholder.com/80x80/1a56db/ffffff?text=SB',
    description: 'Official mobile banking app for SecureBank customers. Manage accounts, transfer funds, and monitor transactions securely.',
  },
  {
    id: 'app-2',
    name: 'SecureBank Business',
    packageId: 'com.securebank.business',
    developer: 'SecureBank Financial Services Inc.',
    storeUrl: 'https://apps.apple.com/app/securebank-business/id123456789',
    logo: 'https://via.placeholder.com/80x80/0d9488/ffffff?text=SB',
    description: 'Business banking solution for SecureBank commercial clients. Multi-user access, approval workflows, and advanced reporting.',
  },
];

export const demoBrandFingerprint: BrandFingerprint = {
  officialBrandName: 'SecureBank',
  normalizedName: 'securebank',
  similarityEngine: 'Levenshtein + Phonetic + Semantic Embedding',
  candidateName: 'SecureBank',
  similarityScore: 100,
};
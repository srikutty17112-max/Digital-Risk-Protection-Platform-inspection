export interface SocialAccount {
  id: string;
  platform: 'instagram' | 'facebook' | 'linkedin' | 'twitter' | 'youtube';
  url: string;
  handle: string;
  verified: boolean;
}

export interface MobileApp {
  id: string;
  name: string;
  packageId: string;
  developer: string;
  storeUrl: string;
  logo: string;
  description: string;
}

export interface BrandProfile {
  id: string;
  brandName: string;
  companyName: string;
  officialWebsite: string;
  description: string;
  keywords: string[];
  aliases: string[];
  logo: string;
}

export interface BrandFingerprint {
  officialBrandName: string;
  normalizedName: string;
  similarityEngine: string;
  candidateName: string;
  similarityScore: number;
}

export interface Module1Data {
  brand: BrandProfile;
  socialAccounts: SocialAccount[];
  mobileApps: MobileApp[];
  brandFingerprint: BrandFingerprint;
}
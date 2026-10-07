import type { SocialAccount } from '../types/brand';

export const platformIcons: Record<SocialAccount['platform'], string> = {
  twitter: 'https://cdn.jsdelivr.net/npm/simple-icons@v13/icons/x.svg',
  linkedin: 'https://cdn.jsdelivr.net/npm/simple-icons@v13/icons/linkedin.svg',
  facebook: 'https://cdn.jsdelivr.net/npm/simple-icons@v13/icons/facebook.svg',
  instagram: 'https://cdn.jsdelivr.net/npm/simple-icons@v13/icons/instagram.svg',
  youtube: 'https://cdn.jsdelivr.net/npm/simple-icons@v13/icons/youtube.svg',
};

export const platformColors: Record<SocialAccount['platform'], string> = {
  twitter: '#000000',
  linkedin: '#0A66C2',
  facebook: '#1877F2',
  instagram: '#E4405F',
  youtube: '#FF0000',
};

export const platformLabels: Record<SocialAccount['platform'], string> = {
  twitter: 'X / Twitter',
  linkedin: 'LinkedIn',
  facebook: 'Facebook',
  instagram: 'Instagram',
  youtube: 'YouTube',
};

export function formatUrl(url: string): string {
  try {
    const u = new URL(url);
    return u.hostname.replace('www.', '');
  } catch {
    return url;
  }
}

export function getInitials(name: string): string {
  return name
    .split(' ')
    .map((n) => n[0])
    .join('')
    .toUpperCase()
    .slice(0, 2);
}
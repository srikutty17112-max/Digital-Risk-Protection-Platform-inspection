export type Platform = 'instagram' | 'facebook' | 'x_twitter' | 'linkedin' | 'youtube' | 'tiktok' | 'other';

export type SourceType = 'LIVE' | 'DEMO' | 'IMPORTED' | 'API' | 'MOCK';

export type ScanStatus = 'PENDING' | 'RUNNING' | 'COMPLETED' | 'FAILED' | 'PARTIAL';

export type ThreatClassification = 'OFFICIAL' | 'LIKELY_LEGITIMATE' | 'SUSPICIOUS' | 'LIKELY_IMPERSONATION' | 'HIGH_RISK_IMPERSONATION';

export type RiskLevel = 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';

export type LookalikePattern = 'CHARACTER_SWAP' | 'ADDED_WORD' | 'REMOVED_CHARACTER' | 'EXTRA_CHARACTER' | 'SPACING_CHANGE' | 'PUNCTUATION_CHANGE' | 'CHARACTER_SUBSTITUTION' | 'CASE_VARIATION';

export type OfficialMatchType = 'EXACT' | 'PARTIAL' | 'NONE';

export type ThreatStatus = 'NEW' | 'REVIEWED' | 'DISMISSED' | 'CONFIRMED' | 'ESCALATED';

export interface CandidateSummary {
  username?: string;
  display_name?: string;
  profile_url?: string;
  bio?: string;
  profile_image_url?: string;
}

export interface Signals {
  name_similarity?: number;
  logo_similarity?: number;
  branding_similarity?: number;
  external_domain_similarity?: number;
}

export interface Lookalike {
  detected: boolean;
  pattern?: LookalikePattern;
  similarity?: number;
  explanation?: string;
}

export interface OfficialMatch {
  is_official: boolean;
  matched_asset_id?: string;
  match_type: OfficialMatchType;
  confidence: number;
}

export interface SocialThreat {
  id: string;
  brand_id: string;
  source_type: string;
  platform: Platform;
  candidate: CandidateSummary;
  signals: Signals;
  lookalike: Lookalike;
  official_match: OfficialMatch;
  risk_score: number;
  risk_level: RiskLevel;
  confidence: number;
  classification: ThreatClassification;
  reasons: string[];
  source: Record<string, unknown>;
  status: ThreatStatus;
}

export interface SocialThreatListResponse {
  threats: SocialThreat[];
  total: number;
  page: number;
  page_size: number;
}

export interface SocialThreatDetailResponse extends SocialThreat {
  collected_at: string;
}

export interface SocialCandidateCreate {
  candidate_id: string;
  brand_id: string;
  platform: Platform;
  username?: string;
  display_name?: string;
  profile_url?: string;
  bio?: string;
  profile_image_url?: string;
  logo_image_url?: string;
  followers_count?: number;
  following_count?: number;
  verification_status?: string;
  external_links?: string[];
  contact_information?: Record<string, unknown>;
  collection_source: SourceType;
}

export interface SocialCandidate {
  candidate_id: string;
  brand_id: string;
  platform: Platform;
  username?: string;
  display_name?: string;
  profile_url?: string;
  bio?: string;
  profile_image_url?: string;
  logo_image_url?: string;
  followers_count?: number;
  following_count?: number;
  verification_status?: string;
  external_links?: string[];
  contact_information?: Record<string, unknown>;
  collection_source: SourceType;
  collected_at: string;
  updated_at: string;
}

export interface SocialCandidateListResponse {
  candidates: SocialCandidate[];
  total: number;
  page: number;
  page_size: number;
}

export interface SocialScanRequest {
  brand_id: string;
  platforms?: Platform[];
  use_demo_data?: boolean;
}

export interface SocialScanJobResponse {
  job_id: string;
  brand_id: string;
  status: ScanStatus;
  platforms?: Platform[];
  total_candidates: number;
  processed_candidates: number;
  threats_found: number;
  official_accounts_found: number;
  error_message?: string;
  started_at?: string;
  completed_at?: string;
  created_at: string;
  updated_at: string;
}

export interface HealthResponse {
  status: string;
  service: string;
  version: string;
  demo_mode: boolean;
}

export interface RootResponse {
  service: string;
  module: number;
  version: string;
  docs: string;
  health: string;
}

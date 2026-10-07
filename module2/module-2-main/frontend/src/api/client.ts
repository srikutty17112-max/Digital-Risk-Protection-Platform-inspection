import type {
  SocialScanRequest,
  SocialScanJobResponse,
  SocialThreatListResponse,
  SocialThreatDetailResponse,
  SocialCandidateListResponse,
  SocialCandidate,
  SocialCandidateCreate,
  HealthResponse,
  RootResponse,
  ThreatStatus,
} from '../types/api';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8001';

async function request<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const url = `${API_BASE_URL}${endpoint}`;
  const response = await fetch(url, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
  });

  if (!response.ok) {
    const text = await response.text();
    throw new Error(`API error ${response.status}: ${text || response.statusText}`);
  }

  if (response.status === 204) {
    return undefined as T;
  }

  return response.json() as Promise<T>;
}

export const api = {
  getRoot(): Promise<RootResponse> {
    return request('/');
  },

  getHealth(): Promise<HealthResponse> {
    return request('/health');
  },

  runScan(data: SocialScanRequest): Promise<SocialScanJobResponse> {
    return request('/api/scan', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  },

  getScanStatus(jobId: string): Promise<SocialScanJobResponse> {
    return request(`/api/scan/${encodeURIComponent(jobId)}`);
  },

  getScanHistory(brandId: string, limit = 20): Promise<SocialScanJobResponse[]> {
    return request(`/api/scan/history/${encodeURIComponent(brandId)}?limit=${limit}`);
  },

  getThreats(params: {
    brand_id: string;
    classification?: string;
    risk_level?: string;
    status?: string;
    include_official?: boolean;
    page?: number;
    page_size?: number;
  }): Promise<SocialThreatListResponse> {
    const searchParams = new URLSearchParams();
    searchParams.set('brand_id', params.brand_id);
    if (params.classification) searchParams.set('classification', params.classification);
    if (params.risk_level) searchParams.set('risk_level', params.risk_level);
    if (params.status) searchParams.set('status', params.status);
    if (params.include_official !== undefined) searchParams.set('include_official', String(params.include_official));
    if (params.page) searchParams.set('page', String(params.page));
    if (params.page_size) searchParams.set('page_size', String(params.page_size));

    return request(`/api/threats?${searchParams.toString()}`);
  },

  getThreat(threatId: string): Promise<SocialThreatDetailResponse> {
    return request(`/api/threats/${encodeURIComponent(threatId)}`);
  },

  updateThreatStatus(threatId: string, newStatus: ThreatStatus): Promise<SocialThreatDetailResponse> {
    return request(`/api/threats/${encodeURIComponent(threatId)}/status?new_status=${encodeURIComponent(newStatus)}`, {
      method: 'PATCH',
    });
  },

  getCandidates(params: {
    brand_id: string;
    platform?: string;
    page?: number;
    page_size?: number;
  }): Promise<SocialCandidateListResponse> {
    const searchParams = new URLSearchParams();
    searchParams.set('brand_id', params.brand_id);
    if (params.platform) searchParams.set('platform', params.platform);
    if (params.page) searchParams.set('page', String(params.page));
    if (params.page_size) searchParams.set('page_size', String(params.page_size));

    return request(`/api/candidates?${searchParams.toString()}`);
  },

  addCandidate(data: SocialCandidateCreate): Promise<SocialCandidate> {
    return request('/api/candidates', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  },

  getCandidate(candidateId: string): Promise<SocialCandidate> {
    return request(`/api/candidates/${encodeURIComponent(candidateId)}`);
  },
};

// Type definitions for Python FastAPI backend

export interface Asset {
  id: number;
  asset_id: string;
  name: string;
  status: string;
  brand?: string;
  model?: string;
  cpu?: string;
  ram?: string;
  hdd?: string;
  purchase_date?: string;
  value?: number;
  location_id?: number;
  assigned_user_id?: number;
  qr_code?: string;
  serial_number?: string;
  category?: string;
  condition?: string;
  description?: string;
  created_at: string;
  updated_at: string;
}

export interface AssetListResponse {
  total: number;
  skip: number;
  limit: number;
  data: Asset[];
}

export interface AssetCreateRequest {
  name: string;
  category_code: string;
  country_id: number;
  province_code: string;
  company_id: number;
  country_code: string;
  company_code: string;
  brand?: string;
  model?: string;
  cpu?: string;
  ram?: string;
  hdd?: string;
  purchase_date?: string;
  value?: number;
  location_id?: number;
  assigned_user_id?: number;
}

export interface AssetUpdateRequest {
  name?: string;
  status?: string;
  brand?: string;
  model?: string;
  cpu?: string;
  ram?: string;
  hdd?: string;
  purchase_date?: string;
  value?: number;
  location_id?: number;
  assigned_user_id?: number;
}

export interface QRCodeResponse {
  asset_id: string;
  qr_code: string;
}

export interface AssetIDPreviewRequest {
  category_code: string;
  country_code: string;
  province_code: string;
  company_code: string;
}

export interface AssetIDPreviewResponse {
  preview: string;
  next_sequence: number;
  year: number;
}

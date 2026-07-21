import { getApiBaseUrl } from '@/lib/proxy';
import { tokenStorage } from '@/services/token-storage';
import type { TokenRefreshResponse } from '@/types/auth';

const API_BASE_URL = getApiBaseUrl();

export interface ApiResponse<T = unknown> {
  error: boolean;
  message: string;
  statusCode: number;
  data: T;
}

function getMessageFromDetail(detail: unknown): string | null {
  if (typeof detail === 'string') {
    return detail;
  }

  if (Array.isArray(detail)) {
    return detail
      .map((item) => {
        if (typeof item === 'string') {
          return item;
        }

        if (item && typeof item === 'object' && 'msg' in item) {
          return String((item as { msg?: unknown }).msg);
        }

        return null;
      })
      .filter(Boolean)
      .join(', ') || null;
  }

  if (detail && typeof detail === 'object') {
    const maybeMessage = (detail as { message?: unknown }).message;
    if (typeof maybeMessage === 'string') {
      return maybeMessage;
    }
  }

  return null;
}

function normalizeApiError<T>(payload: unknown, statusCode: number): ApiResponse<T> {
  if (payload && typeof payload === 'object') {
    const response = payload as Partial<ApiResponse<T>> & { detail?: unknown };
    const message = response.message || getMessageFromDetail(response.detail) || 'Request failed';

    return {
      error: true,
      message,
      statusCode: response.statusCode || statusCode,
      data: (response.data ?? null) as T,
    };
  }

  return {
    error: true,
    message: typeof payload === 'string' ? payload : 'Request failed',
    statusCode,
    data: null as T,
  };
}

class ApiClient {
  private isRefreshing = false;
  private refreshSubscribers: Array<(token: string) => void> = [];

  private onRefreshed(token: string) {
    this.refreshSubscribers.forEach((callback) => callback(token));
    this.refreshSubscribers = [];
  }

  private addRefreshSubscriber(callback: (token: string) => void) {
    this.refreshSubscribers.push(callback);
  }

  async request<T>(endpoint: string, options: RequestInit = {}): Promise<ApiResponse<T>> {
    const url = `${API_BASE_URL}${endpoint}`;
    const headers = new Headers(options.headers || {});
    const token = tokenStorage.getAccessToken();

    if (token && !headers.has('Authorization')) {
      headers.set('Authorization', `Bearer ${token}`);
    }

    if (!(options.body instanceof FormData) && !headers.has('Content-Type')) {
      headers.set('Content-Type', 'application/json');
    }

    try {
      const response = await fetch(url, { ...options, headers });
      const statusCode = response.status;

      if (
        statusCode === 401 &&
        tokenStorage.getRefreshToken() &&
        !endpoint.includes('/auth/refresh') &&
        !endpoint.includes('/auth/login')
      ) {
        return this.handleTokenRefresh<T>(endpoint, options);
      }

      const responseText = await response.text();
      let responseData: ApiResponse<T>;

      try {
        responseData = JSON.parse(responseText);
      } catch {
        throw new Error(responseText || 'Failed to parse JSON response');
      }

      if (!response.ok || responseData.error) {
        throw normalizeApiError<T>(responseData, statusCode);
      }

      return responseData;
    } catch (error) {
      if (typeof error === 'object' && error !== null && 'error' in error) {
        throw error;
      }

      throw {
        error: true,
        message: error instanceof Error ? error.message : 'Unexpected error',
        statusCode: 500,
        data: null,
      } as ApiResponse<T>;
    }
  }

  private async handleTokenRefresh<T>(endpoint: string, options: RequestInit): Promise<ApiResponse<T>> {
    if (this.isRefreshing) {
      return new Promise<ApiResponse<T>>((resolve, reject) => {
        this.addRefreshSubscriber((token) => {
          const headers = new Headers(options.headers || {});
          headers.set('Authorization', `Bearer ${token}`);
          this.request<T>(endpoint, { ...options, headers }).then(resolve).catch(reject);
        });
      });
    }

    this.isRefreshing = true;

    try {
      const refreshToken = tokenStorage.getRefreshToken();
      if (!refreshToken) {
        throw new Error('No refresh token available');
      }

      const refreshResponse = await fetch(`${API_BASE_URL}/auth/refresh`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ refresh_token: refreshToken }),
      });

      if (!refreshResponse.ok) {
        throw new Error('Refresh token is invalid or expired');
      }

      const refreshResult: ApiResponse<TokenRefreshResponse> = await refreshResponse.json();
      if (refreshResult.error || !refreshResult.data) {
        throw new Error(refreshResult.message || 'Refresh failed');
      }

      const { access_token: accessToken, refresh_token: nextRefreshToken } = refreshResult.data;
      tokenStorage.setTokens(accessToken, nextRefreshToken);
      this.isRefreshing = false;
      this.onRefreshed(accessToken);

      const headers = new Headers(options.headers || {});
      headers.set('Authorization', `Bearer ${accessToken}`);
      return this.request<T>(endpoint, { ...options, headers });
    } catch {
      this.isRefreshing = false;
      tokenStorage.clearSession();

      if (typeof window !== 'undefined') {
        window.dispatchEvent(new CustomEvent('auth:expired'));
      }

      throw {
        error: true,
        message: 'Session expired. Please log in again.',
        statusCode: 401,
        data: null,
      } as ApiResponse<T>;
    }
  }

  get<T>(endpoint: string, options: RequestInit = {}) {
    return this.request<T>(endpoint, { ...options, method: 'GET' });
  }

  post<T>(endpoint: string, body?: unknown, options: RequestInit = {}) {
    return this.request<T>(endpoint, {
      ...options,
      method: 'POST',
      body: body instanceof FormData ? body : JSON.stringify(body),
    });
  }

  patch<T>(endpoint: string, body?: unknown, options: RequestInit = {}) {
    return this.request<T>(endpoint, {
      ...options,
      method: 'PATCH',
      body: body instanceof FormData ? body : JSON.stringify(body),
    });
  }

  delete<T>(endpoint: string, options: RequestInit = {}) {
    return this.request<T>(endpoint, { ...options, method: 'DELETE' });
  }
}

export const apiClient = new ApiClient();

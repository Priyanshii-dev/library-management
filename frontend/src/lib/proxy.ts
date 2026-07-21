export function getApiBaseUrl() {
  if (typeof window !== 'undefined') {
    return '/api/v1';
  }

  return process.env.NEXT_PUBLIC_API_URL || '/api/v1';
}

export type UserRole = 'Admin' | 'User';

export interface AuthSession {
  accessToken: string;
  refreshToken: string;
  userRole: UserRole;
  userId: number;
  userEmail: string;
}

export interface TokenRefreshResponse {
  access_token: string;
  refresh_token: string;
}

export interface LoginResponse extends TokenRefreshResponse {
  user_role: UserRole;
  user_id: number;
  email: string;
}

export interface UserProfile {
  id: number;
  first_name: string;
  last_name: string;
  email: string;
  phone: string | null;
  role: string;
  status: string;
  user_logo: string | null;
  created_at: string;
  updated_at: string;
}

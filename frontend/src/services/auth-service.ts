import { apiClient } from '@/services/api-client';
import type {
  ForgotPasswordInput,
  LoginInput,
  OtpInput,
  ProfileUpdateInput,
  RegisterInput,
  ResetPasswordInput,
} from '@/lib/schemas';
import type { LoginResponse, UserProfile } from '@/types/auth';

export const authService = {
  async login(data: LoginInput) {
    return apiClient.post<LoginResponse>('/auth/login', {
      email: data.email,
      password: data.password,
    });
  },

  async register(data: RegisterInput) {
    return apiClient.post<{ email: string }>('/auth/register', {
      first_name: data.first_name,
      last_name: data.last_name,
      phone: data.phone,
      email: data.email,
      password: data.password,
    });
  },

  async verifyEmail(data: OtpInput) {
    return apiClient.post<{ email_verified: boolean; user_id: number }>('/auth/verify-email', {
      email: data.email,
      otp_code: data.otp_code,
    });
  },

  async resendOtp(email: string) {
    return apiClient.post<{ email: string; user_id: number }>(`/auth/resend-otp?email=${encodeURIComponent(email)}`);
  },

  async forgotPassword(data: ForgotPasswordInput) {
    return apiClient.post('/auth/forgot-password', { email: data.email });
  },

  async resetPassword(data: ResetPasswordInput) {
    return apiClient.post('/auth/reset-password', {
      email: data.email,
      otp_code: data.otp_code,
      new_password: data.new_password,
    });
  },

  async getProfile() {
    return apiClient.get<UserProfile>('/users/me');
  },

  async updateProfile(userId: number, data: ProfileUpdateInput) {
    return apiClient.patch<UserProfile>(`/users/${userId}`, data);
  },

  async logout() {
    return apiClient.post('/auth/logout');
  },
};

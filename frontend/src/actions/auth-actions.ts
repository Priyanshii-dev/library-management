import { authService } from '@/services/auth-service';
import { tokenStorage } from '@/services/token-storage';
import type {
  ForgotPasswordInput,
  LoginInput,
  OtpInput,
  ProfileUpdateInput,
  RegisterInput,
  ResetPasswordInput,
} from '@/lib/schemas';

export const authActions = {
  async login(data: LoginInput) {
    const response = await authService.login(data);

    if (response.data) {
      tokenStorage.setSession({
        accessToken: response.data.access_token,
        refreshToken: response.data.refresh_token,
        userRole: response.data.user_role,
        userId: response.data.user_id,
        userEmail: response.data.email,
      });
    }

    return response;
  },

  register(data: RegisterInput) {
    return authService.register(data);
  },

  verifyEmail(data: OtpInput) {
    return authService.verifyEmail(data);
  },

  resendOtp(email: string) {
    return authService.resendOtp(email);
  },

  forgotPassword(data: ForgotPasswordInput) {
    return authService.forgotPassword(data);
  },

  resetPassword(data: ResetPasswordInput) {
    return authService.resetPassword(data);
  },

  getProfile() {
    return authService.getProfile();
  },

  updateProfile(userId: number, data: ProfileUpdateInput) {
    return authService.updateProfile(userId, data);
  },

  async logout() {
    try {
      await authService.logout();
    } finally {
      tokenStorage.clearSession();
    }
  },
};

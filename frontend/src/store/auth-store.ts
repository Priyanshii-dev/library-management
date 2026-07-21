import { create } from 'zustand';
import { authActions } from '@/actions/auth-actions';
import { LoginInput, RegisterInput, ProfileUpdateInput, ForgotPasswordInput, ResetPasswordInput, OtpInput } from '@/lib/schemas';
import { tokenStorage } from '@/services/token-storage';
import type { UserProfile, UserRole } from '@/types/auth';

interface AuthState {
  isAuthenticated: boolean;
  isCheckingAuth: boolean;
  userRole: UserRole | null;
  userId: number | null;
  userEmail: string | null;
  userProfile: UserProfile | null;
  registeredEmail: string | null;
  login: (data: LoginInput) => Promise<string>;
  register: (data: RegisterInput) => Promise<string>;
  verifyEmail: (data: OtpInput) => Promise<string>;
  resendOtp: (email: string) => Promise<string>;
  forgotPassword: (data: ForgotPasswordInput) => Promise<string>;
  resetPassword: (data: ResetPasswordInput) => Promise<string>;
  getProfile: () => Promise<UserProfile>;
  updateProfile: (data: ProfileUpdateInput) => Promise<string>;
  logout: () => Promise<void>;
  initializeAuth: () => Promise<void>;
  setRegisteredEmail: (email: string | null) => void;
}

export const useAuthStore = create<AuthState>((set, get) => ({
  isAuthenticated: false,
  isCheckingAuth: true,
  userRole: null,
  userId: null,
  userEmail: null,
  userProfile: null,
  registeredEmail: null,

  setRegisteredEmail: (email) => set({ registeredEmail: email }),

  initializeAuth: async () => {
    set({ isCheckingAuth: true });
    const session = tokenStorage.getSession();

    if (session) {
      set({
        isAuthenticated: true,
        userRole: session.userRole,
        userId: session.userId,
        userEmail: session.userEmail,
      });
      try {
        await get().getProfile();
      } catch {
        tokenStorage.clearSession();
        set({ isAuthenticated: false, userRole: null, userId: null, userEmail: null, userProfile: null });
      }
    }

    set({ isCheckingAuth: false });
  },

  login: async (data) => {
    const res = await authActions.login(data);

    if (res.data) {
      const { user_role, user_id, email } = res.data;
      set({ isAuthenticated: true, userRole: user_role, userId: user_id, userEmail: email });
      await get().getProfile();
    }

    return res.message || 'Logged in successfully';
  },

  register: async (data) => {
    const res = await authActions.register(data);
    set({ registeredEmail: data.email });
    return res.message || 'Registration successful';
  },

  verifyEmail: async (data) => {
    const res = await authActions.verifyEmail(data);
    return res.message || 'Email verified successfully';
  },

  resendOtp: async (email) => {
    const res = await authActions.resendOtp(email);
    set({ registeredEmail: email });
    return res.message || 'OTP sent';
  },

  forgotPassword: async (data) => {
    const res = await authActions.forgotPassword(data);
    return res.message || 'OTP sent';
  },

  resetPassword: async (data) => {
    const res = await authActions.resetPassword(data);
    return res.message || 'Password reset successful';
  },

  getProfile: async () => {
    const res = await authActions.getProfile();
    set({ userProfile: res.data });
    return res.data;
  },

  updateProfile: async (data) => {
    const userId = get().userId ?? get().userProfile?.id;
    if (!userId) {
      throw new Error('Unable to update profile without a signed-in user.');
    }

    const res = await authActions.updateProfile(userId, data);
    set({ userProfile: res.data });
    return res.message || 'Profile updated';
  },

  logout: async () => {
    await authActions.logout();
    set({ isAuthenticated: false, userRole: null, userId: null, userEmail: null, userProfile: null, registeredEmail: null });
  },
}));

if (typeof window !== 'undefined') {
  window.addEventListener('auth:expired', () => {
    void useAuthStore.getState().logout();
  });
}

import type { AuthSession, UserRole } from '@/types/auth';

const ACCESS_TOKEN_KEY = 'access_token';
const REFRESH_TOKEN_KEY = 'refresh_token';
const USER_ROLE_KEY = 'user_role';
const USER_ID_KEY = 'user_id';
const USER_EMAIL_KEY = 'user_email';

function getStorage() {
  if (typeof window === 'undefined') {
    return null;
  }

  return window.localStorage;
}

export const tokenStorage = {
  getAccessToken() {
    return getStorage()?.getItem(ACCESS_TOKEN_KEY) ?? null;
  },

  getRefreshToken() {
    return getStorage()?.getItem(REFRESH_TOKEN_KEY) ?? null;
  },

  getSession(): AuthSession | null {
    const storage = getStorage();
    if (!storage) {
      return null;
    }

    const accessToken = storage.getItem(ACCESS_TOKEN_KEY);
    const refreshToken = storage.getItem(REFRESH_TOKEN_KEY);
    const userRole = storage.getItem(USER_ROLE_KEY) as UserRole | null;
    const userId = storage.getItem(USER_ID_KEY);
    const userEmail = storage.getItem(USER_EMAIL_KEY);

    if (!accessToken || !refreshToken || !userRole || !userId || !userEmail) {
      return null;
    }

    return {
      accessToken,
      refreshToken,
      userRole,
      userId: Number(userId),
      userEmail,
    };
  },

  setTokens(accessToken: string, refreshToken: string) {
    const storage = getStorage();
    if (!storage) {
      return;
    }

    storage.setItem(ACCESS_TOKEN_KEY, accessToken);
    storage.setItem(REFRESH_TOKEN_KEY, refreshToken);
  },

  setSession(session: AuthSession) {
    const storage = getStorage();
    if (!storage) {
      return;
    }

    storage.setItem(ACCESS_TOKEN_KEY, session.accessToken);
    storage.setItem(REFRESH_TOKEN_KEY, session.refreshToken);
    storage.setItem(USER_ROLE_KEY, session.userRole);
    storage.setItem(USER_ID_KEY, String(session.userId));
    storage.setItem(USER_EMAIL_KEY, session.userEmail);
  },

  clearSession() {
    const storage = getStorage();
    if (!storage) {
      return;
    }

    storage.removeItem(ACCESS_TOKEN_KEY);
    storage.removeItem(REFRESH_TOKEN_KEY);
    storage.removeItem(USER_ROLE_KEY);
    storage.removeItem(USER_ID_KEY);
    storage.removeItem(USER_EMAIL_KEY);
  },
};

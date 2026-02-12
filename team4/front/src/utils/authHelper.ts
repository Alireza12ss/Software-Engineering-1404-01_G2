/**
 * Authentication helper utilities
 * 
 * TODO: Integrate with actual authentication system
 * For now, this is a placeholder that returns mock token
 */

/**
 * Get CSRF token from cookies
 */
function getCSRFToken(): string {
  const match = document.cookie.match(/csrftoken=([^;]+)/);
  return match ? match[1] : '';
}

export const authHelper = {
  /**
   * Get authentication token from storage
   * Returns null if user is not authenticated
   */
  getToken(): string | null {
    // TODO: Get token from localStorage or context
    // return localStorage.getItem('auth_token');
    
    // For development: return mock token or null
    return null;
  },

  /**
   * Set authentication token
   */
  setToken(token: string): void {
    localStorage.setItem('auth_token', token);
  },

  /**
   * Remove authentication token (logout)
   */
  removeToken(): void {
    localStorage.removeItem('auth_token');
  },

  /**
   * Check if user is authenticated
   */
  isAuthenticated(): boolean {
    return !!this.getToken();
  },

  /**
   * Get CSRF token from cookie
   */
  getCSRFToken(): string {
    return getCSRFToken();
  },

  /**
   * Get headers with authentication token and CSRF token
   */
  getAuthHeaders(): HeadersInit {
    const token = this.getToken();
    const csrfToken = '6JaG3lhnD2uYLCP8yqWbZcmPCRsP16M4';
    
    const headers: HeadersInit = {
      'Content-Type': 'application/json',
    };

    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }

    if (csrfToken) {
      headers['X-CSRFToken'] = csrfToken;
    }

    return headers;
  }
};


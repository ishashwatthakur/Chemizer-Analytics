const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 
  (typeof window !== 'undefined' && window.location.hostname !== 'localhost' 
    ? `https://${window.location.hostname.replace('-5173', '-8000').replace('-5000', '-8000')}/api`
    : 'http://127.0.0.1:8000/api');

interface ApiResponse<T = unknown> {
  data?: T;
  error?: string;
}

interface UserData {
  user_id: string | number;
  username: string;
  email: string;
  full_name?: string;
  date_of_birth?: string;
  gender?: string;
}

class APIClient {
  private token: string | null = null;

  constructor() {
    // Load token from localStorage on init
    this.token = localStorage.getItem('auth_token');
  }

  private getHeaders(): HeadersInit {
    const headers: HeadersInit = {
      'Content-Type': 'application/json',
    };
    
    if (this.token) {
      headers['Authorization'] = `Token ${this.token}`;
    }
    
    return headers;
  }

  setToken(token: string | null) {
    this.token = token;
    if (token) {
      localStorage.setItem('auth_token', token);
      localStorage.setItem('isAuthenticated', 'true');
    } else {
      localStorage.removeItem('auth_token');
      localStorage.removeItem('isAuthenticated');
      localStorage.removeItem('user_data');
    }
  }

  getToken(): string | null {
    return this.token;
  }

  setUserData(userData: UserData) {
    localStorage.setItem('user_data', JSON.stringify(userData));
  }

  getUserData(): UserData | null {
    const data = localStorage.getItem('user_data');
    return data ? JSON.parse(data) : null;
  }

  async register(data: {
    username: string;
    email: string;
    password: string;
    full_name?: string;
    date_of_birth?: string;
    gender?: string;
  }): Promise<ApiResponse> {
    try {
      console.log('Registering user:', data.username);
      
      const response = await fetch(`${API_BASE_URL}/auth/register/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
      });

      const result = await response.json();
      console.log('Registration response:', result);

      if (!response.ok) {
        return { error: this.formatError(result) };
      }

      return { data: result };
    } catch (error) {
      console.error('Registration error:', error);
      return { error: 'Network error. Please check if Django server is running.' };
    }
  }

  async login(username: string, password: string): Promise<ApiResponse> {
    try {
      console.log('Logging in user:', username);
      
      const response = await fetch(`${API_BASE_URL}/auth/login/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password }),
      });

      const result = await response.json();
      console.log('Login response:', result);

      if (!response.ok) {
        return { error: this.formatError(result) };
      }

      // ✅ FIXED: Set login timestamp for 48-hour session
      if (result.token) {
        this.setToken(result.token);
        this.setUserData({
          user_id: result.user_id,
          username: result.username,
          email: result.email,
          full_name: result.full_name,
        });
        // Set login timestamp for session expiry (48 hours)
        localStorage.setItem('login_timestamp', Date.now().toString());
      }

      return { data: result };
    } catch (error) {
      console.error('Login error:', error);
      return { error: 'Network error. Please check if Django server is running.' };
    }
  }

  async verifyOTP(email: string, otp: string): Promise<ApiResponse> {
    try {
      console.log('Verifying OTP for:', email);
      
      const response = await fetch(`${API_BASE_URL}/auth/verify-otp/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, otp }),
      });

      const result = await response.json();
      console.log('OTP verification response:', result);

      if (!response.ok) {
        return { error: this.formatError(result) };
      }

      // Save token and user data
      if (result.token) {
        this.setToken(result.token);
        this.setUserData({
          user_id: result.user_id,
          username: result.username,
          email: result.email,
          full_name: result.full_name,
        });
      }

      return { data: result };
    } catch (error) {
      console.error('OTP verification error:', error);
      return { error: 'Network error. Please try again.' };
    }
  }

  async resendOTP(email: string): Promise<ApiResponse> {
    try {
      const response = await fetch(`${API_BASE_URL}/auth/resend-otp/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email }),
      });

      const result = await response.json();

      if (!response.ok) {
        return { error: this.formatError(result) };
      }

      return { data: result };
    } catch (error) {
      return { error: 'Network error. Please try again.' };
    }
  }

  async getProfile(): Promise<ApiResponse> {
    try {
      const response = await fetch(`${API_BASE_URL}/auth/profile/`, {
        method: 'GET',
        headers: this.getHeaders(),
      });

      const result = await response.json();

      if (!response.ok) {
        return { error: this.formatError(result) };
      }

      // Update local user data
      this.setUserData(result);

      return { data: result };
    } catch (error) {
      return { error: 'Network error. Please try again.' };
    }
  }

  async updateProfile(data: {
    full_name?: string;
    date_of_birth?: string;
    gender?: string;
  }): Promise<ApiResponse> {
    try {
      const response = await fetch(`${API_BASE_URL}/auth/profile/update/`, {
        method: 'PUT',
        headers: this.getHeaders(),
        body: JSON.stringify(data),
      });

      const result = await response.json();

      if (!response.ok) {
        return { error: this.formatError(result) };
      }

      // Update local user data
      const userData = this.getUserData();
      if (userData) {
        this.setUserData({ ...userData, ...result.data });
      }

      return { data: result };
    } catch (error) {
      return { error: 'Network error. Please try again.' };
    }
  }

  async deleteAccount(): Promise<ApiResponse> {
    try {
      const response = await fetch(`${API_BASE_URL}/auth/profile/delete/`, {
        method: 'DELETE',
        headers: this.getHeaders(),
      });

      if (!response.ok) {
        return { error: 'Failed to delete account' };
      }

      this.logout();
      return { data: { success: true } };
    } catch (error) {
      return { error: 'Network error. Please try again.' };
    }
  }

  async googleLogin(googleToken: string): Promise<ApiResponse> {
    try {
      console.log('Google login with token');
      
      const response = await fetch(`${API_BASE_URL}/auth/google/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ token: googleToken }),
      });

      const result = await response.json();
      console.log('Google login response:', result);

      if (!response.ok) {
        return { error: this.formatError(result) };
      }

      // Save token and user data
      if (result.token) {
        this.setToken(result.token);
        this.setUserData({
          user_id: result.user_id,
          username: result.username,
          email: result.email,
          full_name: result.full_name,
        });
      }

      return { data: result };
    } catch (error) {
      console.error('Google login error:', error);
      return { error: 'Network error. Please try again.' };
    }
  }

  async uploadFile(file: File, onProgress?: (progress: number) => void): Promise<ApiResponse> {
    try {
      console.log('Uploading file:', file.name);
      
      const formData = new FormData();
      formData.append('file', file);

      const xhr = new XMLHttpRequest();
      
      return new Promise((resolve) => {
        xhr.upload.addEventListener('progress', (e) => {
          if (e.lengthComputable && onProgress) {
            const progress = Math.round((e.loaded / e.total) * 100);
            onProgress(progress);
          }
        });

        xhr.addEventListener('load', () => {
          try {
            const result = JSON.parse(xhr.responseText);
            
            if (xhr.status === 200 || xhr.status === 201) {
              console.log('Upload successful:', result);
              resolve({ data: result });
            } else {
              console.error('Upload failed:', result);
              resolve({ error: this.formatError(result) });
            }
          } catch (error) {
            resolve({ error: 'Failed to parse server response' });
          }
        });

        xhr.addEventListener('error', () => {
          resolve({ error: 'Network error during upload' });
        });

        xhr.open('POST', `${API_BASE_URL}/auth/upload/`);
        if (this.token) {
          xhr.setRequestHeader('Authorization', `Token ${this.token}`);
        }
        xhr.send(formData);
      });
    } catch (error) {
      console.error('Upload error:', error);
      return { error: 'Failed to upload file' };
    }
  }

  async getUploadHistory(): Promise<ApiResponse> {
    try {
      const response = await fetch(`${API_BASE_URL}/auth/uploads/history/`, {
        method: 'GET',
        headers: this.getHeaders(),
      });

      const result = await response.json();

      if (!response.ok) {
        return { error: this.formatError(result) };
      }

      return { data: result };
    } catch (error) {
      return { error: 'Network error. Please try again.' };
    }
  }

  async getUploadDetail(uploadId: string): Promise<ApiResponse> {
    try {
      const response = await fetch(`${API_BASE_URL}/auth/uploads/${uploadId}/`, {
        method: 'GET',
        headers: this.getHeaders(),
      });

      const result = await response.json();

      if (!response.ok) {
        return { error: this.formatError(result) };
      }

      return { data: result };
    } catch (error) {
      return { error: 'Network error. Please try again.' };
    }
  }

  async deleteUpload(uploadId: string): Promise<ApiResponse> {
    try {
      const response = await fetch(`${API_BASE_URL}/auth/uploads/${uploadId}/delete/`, {
        method: 'DELETE',
        headers: this.getHeaders(),
      });

      if (!response.ok) {
        const result = await response.json();
        return { error: this.formatError(result) };
      }

      return { data: { success: true } };
    } catch (error) {
      return { error: 'Network error. Please try again.' };
    }
  }

  async downloadPDFReport(uploadId: string): Promise<Blob | null> {
    try {
      const response = await fetch(`${API_BASE_URL}/reports/download/${uploadId}/`, {
        method: 'GET',
        headers: {
          'Authorization': this.token ? `Token ${this.token}` : '',
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        console.error(`Failed to download report: ${response.status} ${response.statusText}`);
        const errorText = await response.text();
        console.error('Error response:', errorText);
        return null;
      }

      const blob = await response.blob();
      if (blob.size === 0) {
        console.error('Downloaded file is empty');
        return null;
      }

      return blob;
    } catch (error) {
      console.error('Download error:', error);
      return null;
    }
  }

  async bulkDeleteUploads(uploadIds: string[]): Promise<ApiResponse> {
    try {
      const response = await fetch(`${API_BASE_URL}/auth/uploads/bulk-delete/`, {
        method: 'POST',
        headers: this.getHeaders(),
        body: JSON.stringify({ upload_ids: uploadIds }),
      });

      const result = await response.json();
      if (!response.ok) {
        return { error: this.formatError(result) };
      }
      return { data: result };
    } catch (error) {
      return { error: 'Network error. Please try again.' };
    }
  }

  async downloadAllData(): Promise<Blob | null> {
    try {
      const response = await fetch(`${API_BASE_URL}/auth/data/download-all/`, {
        method: 'GET',
        headers: { 'Authorization': this.token ? `Token ${this.token}` : '' },
      });

      if (!response.ok) {
        return null;
      }
      return await response.blob();
    } catch (error) {
      return null;
    }
  }

  async deleteAllData(): Promise<ApiResponse> {
    try {
      const response = await fetch(`${API_BASE_URL}/auth/data/delete-all/`, {
        method: 'POST',
        headers: this.getHeaders(),
      });

      const result = await response.json();
      if (!response.ok) {
        return { error: this.formatError(result) };
      }
      return { data: result };
    } catch (error) {
      return { error: 'Network error. Please try again.' };
    }
  }

  logout() {
    this.setToken(null);
  }

  isAuthenticated(): boolean {
    return this.token !== null && localStorage.getItem('isAuthenticated') === 'true';
  }

  private formatError(error: unknown): string {
    if (typeof error === 'string') {
      return error;
    }

    if (error && typeof error === 'object' && 'error' in error) {
      return String(error.error);
    }

    if (error && typeof error === 'object') {
      const errors: string[] = [];
      for (const [field, messages] of Object.entries(error)) {
        if (Array.isArray(messages)) {
          errors.push(`${field}: ${messages.join(', ')}`);
        } else {
          errors.push(`${field}: ${messages}`);
        }
      }
      return errors.join('\n');
    }

    return 'An error occurred';
  }
}

export const apiClient = new APIClient();
import { IMsg, IToken, IUser } from '../schema';
import request from '@/utils/request';

const api = {
  async loginAccessToken(username: string, password: string): Promise<IToken> {
    const data = new URLSearchParams();
    data.append('username', username);
    data.append('password', password);

    return request.post(
      '/login/access-token',
      data,
      {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
      },
    );
  },

  async logout(): Promise<IMsg> {
    return request.post('/logout');
  },

  async testToken(): Promise<IUser> {
    return request.post('/login/test-token');
  },

  async updateLoginMe(password: string, newEmail?: string, newPassword?: string): Promise<IUser> {
    const data = { password, newEmail, newPassword };
    return request.post('/login/update', data);
  },

  async recoverPassword(email: string): Promise<IMsg> {
    return request.post(`/password-recovery/${email}`);
  },

  async resetPassword(token: string, newPassword: string): Promise<IMsg> {
    const data = { token, newPassword };
    return request.post('/reset-password/', data);
  },

};

export default api;

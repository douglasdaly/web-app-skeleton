import { IToken, IUser } from '../schema';
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

  async testToken(): Promise<IUser> {
    return request.post('/login/test-token');
  },
};

export default api;

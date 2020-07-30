import request from '@/utils/request';
import { IUser } from '@/api/schema';

const BASE_URL = '/users';

const api = {
  async readUserMe(): Promise<IUser> {
    return request.get(`${BASE_URL}/me`);
  },
};

export default api;

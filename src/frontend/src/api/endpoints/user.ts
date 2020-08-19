import request from '@/utils/request';
import { INameUpdate, IUser, IUserCreate, INameCreate, IUserUpdate } from '@/api/schema';

const BASE_URL = '/users';

function getApiUrl(endpoint?: string): string {
  if (endpoint) {
    return `${BASE_URL}/${endpoint}`;
  }
  return `${BASE_URL}/`;
}


const api = {
  async readUsers(): Promise<Array<IUser>> {
    return request.get(getApiUrl());
  },

  async readUserMe(): Promise<IUser> {
    return request.get(getApiUrl('me'));
  },

  async readUserById(userId: string): Promise<IUser> {
    return request.get(getApiUrl(userId));
  },

  async createUser(user: IUserCreate): Promise<IUser> {
    return request.post(getApiUrl(), user);
  },

  async createUserOpen(
    email: string,
    password: string,
    name?: INameCreate,
  ): Promise<IUser> {
    const data = { email, password, name };
    return request.post(getApiUrl('open'), data);
  },

  async updateUser(userId: string, userIn: IUserUpdate): Promise<IUser> {
    return request.put(getApiUrl(userId), userIn);
  },

  async updateUserMe(name: INameUpdate): Promise<IUser> {
    return request.put(getApiUrl('me'), { ...name });
  },

};

export default api;

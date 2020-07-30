import authApi from './endpoints/auth';
import userApi from './endpoints/user';

const api = {
  auth: authApi,
  user: userApi,
};

export default api;

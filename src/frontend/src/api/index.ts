import authApi from './endpoints/auth';
import rolesApi from './endpoints/roles';
import usersApi from './endpoints/user';

const api = {
  auth: authApi,
  roles: rolesApi,
  user: usersApi,
};

export default api;

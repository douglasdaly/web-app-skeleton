import { IRole, IRoleCreate, IRoleUpdate } from '../schema';
import request from '@/utils/request';

const BASE_URL = '/roles';

function getApiUrl(endpoint?: string): string {
  if (endpoint) {
    return `${BASE_URL}/${endpoint}`;
  }
  return `${BASE_URL}/`;
}

const api = {
  async readRoleById(roleId: string): Promise<IRole> {
    return request.get(getApiUrl(roleId));
  },

  async readRoleCount(): Promise<number> {
    return request.get(getApiUrl('count'));
  },

  async readRoles(skip?: number, limit?: number): Promise<Array<IRole>> {
    return request.get(getApiUrl(), { params: { skip, limit } });
  },

  async createRole(role: IRoleCreate): Promise<IRole> {
    return request.post(getApiUrl(), role);
  },

  async updateRole(roleId: string, roleIn: IRoleUpdate): Promise<IRole> {
    return request.put(getApiUrl(roleId), roleIn);
  },

  async deleteRole(roleId: string): Promise<void> {
    return request.delete(getApiUrl(roleId));
  },
};

export default api;

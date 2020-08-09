import Cookies from 'js-cookie';

import { appName } from '@/env';

// Constants
const BASE_KEY = appName.toLowerCase().replace(' ', '_');
function getKey(key: string): string {
  return `${BASE_KEY}-${key}`;
}

// Application
const drawerStatusKey = getKey('sidebar_status');

export function getDrawerStatus(): string | undefined {
  return Cookies.get(drawerStatusKey);
}

export function setDrawerStatus(status: string) {
  Cookies.set(drawerStatusKey, status);
}

// Auth
const tokenKey = getKey('token');

export function getToken(): string | undefined {
  return Cookies.get(tokenKey);
}

export function setToken(token: string) {
  Cookies.set(tokenKey, token);
}

export function removeToken() {
  Cookies.remove(tokenKey);
}

// Export all
const cookieFunctions = {
  getDrawerStatus,
  setDrawerStatus,
  getToken,
  setToken,
  removeToken,
};

export default cookieFunctions;

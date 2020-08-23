import Cookies from 'js-cookie';

import { appName } from '@/env';

// Constants
const BASE_KEY = appName.toLowerCase().replace(' ', '_');
function getKey(key: string): string {
  return `${BASE_KEY}-${key}`;
}

// Application
// - Drawer Status
const drawerStatusKey = getKey('sidebar_status');

export function getDrawerStatus(): string | undefined {
  return Cookies.get(drawerStatusKey);
}

export function setDrawerStatus(status: string) {
  Cookies.set(drawerStatusKey, status);
}

// - Cookies notified
const cookieNotifyKey = getKey('cookies_notified');

export function getCookiesNotified(): boolean | undefined {
  return Cookies.get(cookieNotifyKey) === 'true';
}

export function setCookiesNotified(notified: boolean) {
  Cookies.set(cookieNotifyKey, notified ? 'true' : 'false');
}

export function removeCookiesNotified() {
  Cookies.remove(cookieNotifyKey);
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
  getCookiesNotified,
  setCookiesNotified,
  removeCookiesNotified,
  getToken,
  setToken,
  removeToken,
};

export default cookieFunctions;

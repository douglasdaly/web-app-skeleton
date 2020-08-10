import { appName } from '@/env';

// General
const BASE_KEY = appName.toLowerCase().replace(' ', '_');

function getKey(key: string) {
  return `${BASE_KEY}-${key}`;
}

export const getLocal = (key: string) => {
  return window.localStorage.getItem(getKey(key));
}

export const setLocal = (key: string, value: any) => {
  return window.localStorage.setItem(getKey(key), value);
}

export const removeLocal = (key: string) => {
  return window.localStorage.removeItem(getKey(key));
}

// Tokens
const TOKEN_KEY = "token";

export const getLocalToken = () => {
  return getLocal(TOKEN_KEY);
};

export const saveLocalToken = (token: string) => {
  return setLocal(TOKEN_KEY, token);
};

export const removeLocalToken = () => {
  return removeLocal(TOKEN_KEY);
};

export default {
  getLocal,
  setLocal,
  removeLocal,
  getLocalToken,
  saveLocalToken,
  removeLocalToken,
};

const TOKEN_KEY = "token";

export const getLocalToken = () => {
  return window.localStorage.getItem(TOKEN_KEY);
};

export const saveLocalToken = (token: string) => {
  return window.localStorage.setItem(TOKEN_KEY, token);
};

export const removeLocalToken = () => {
  return window.localStorage.removeItem(TOKEN_KEY);
};

export default { getLocalToken, saveLocalToken, removeLocalToken };

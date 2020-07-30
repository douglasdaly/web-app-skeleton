import axios, { AxiosRequestConfig, AxiosResponse } from 'axios';

import { apiURL } from '@/env';
import AuthModule from '@/store/modules/auth';

const service = axios.create({
  baseURL: apiURL,
  timeout: 5000,
});

// Request interceptors
service.interceptors.request.use(
  function (config: AxiosRequestConfig) {
    const token = AuthModule.token;
    if (token) {
      config.headers.common.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  function (error) {
    return Promise.reject(error);
  },
);

// Response interceptors
service.interceptors.response.use(
  function (response: AxiosResponse) {
    const res = response.data;
    if (response.status !== 200) {
      return Promise.reject(new Error(res.message || 'Error'));
    }
    return res;
  },
  function (error) {
    return Promise.reject(error);
  },
);

export default service;

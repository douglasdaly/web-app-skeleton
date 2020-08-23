export const env = process.env.NODE_ENV;

// General
export const appName = process.env.VUE_APP_NAME;

// Backend API
const envApiProto = process.env.VUE_APP_API_PROTOCOL || 'http';
const envApiDomain = process.env.VUE_APP_API_DOMAIN || 'localhost';
const envApiBaseURL = process.env.VUE_APP_API_BASE || '/api';
export const apiURL = `${envApiProto}://${envApiDomain}${envApiBaseURL}`;

export const env = process.env.NODE_ENV;

// General
export const appName = process.env.VUE_APP_NAME;

// Backend API
let envApiProto = 'https';
let envApiDomain = '';
if (env === 'production') {
  envApiDomain = process.env.VUE_APP_API_DOMAIN_PROD || process.env.VUE_APP_DOMAIN_PROD;
} else if (env === 'staging') {
  envApiDomain = process.env.VUE_APP_API_DOMAIN_STAGE || process.env.VUE_APP_DOMAIN_STAGE;
} else {
  envApiProto = 'http';
  envApiDomain = process.env.VUE_APP_API_DOMAIN_DEV || process.env.VUE_APP_DOMAIN_DEV;
}
const envApiBaseURL = process.env.VUE_APP_API_BASE || '';

export const apiURL = `${envApiProto}://${envApiDomain}${envApiBaseURL}`;

import Vue from 'vue';
import VueRouter, { Route, RouteConfig } from 'vue-router';

import AuthModule from '@/store/modules/auth';
import RoutesModule from '@/store/modules/routes';

import AccountLayout from '@/layouts/AccountLayout.vue';
import DefaultLayout from '@/layouts/DefaultLayout.vue';

import adminRoutes from './modules/admin';

Vue.use(VueRouter);

/**
 * Constant Routes
 *
 * These routes are available to all visitors.
 */
export const constantRoutes: RouteConfig[] = [
  {
    path: '/',
    component: DefaultLayout,
    redirect: '/index',
    children: [
      {
        path: 'index',
        component: () => import(/* webpackChunkName: "home" */ '@/views/Home.vue'),
        name: 'Home',
        meta: {
          title: 'Home',
          icon: 'mdi-home',
        },
      },
    ],
  },
  {
    path: '/',
    component: DefaultLayout,
    redirect: '/about',
    children: [
      {
        path: 'about',
        name: 'About',
        component: () => import(/* webpackChunkName: "about" */ '../views/About.vue'),
        meta: {
          title: 'About',
          icon: 'mdi-help-box',
        },
      },
    ],
  },
  {
    path: '/',
    component: DefaultLayout,
    redirect: '/login',
    meta: {
      hidden: true,
    },
    children: [
      {
        path: 'login',
        name: 'Login',
        component: () => import(/* webpackChunkName: "login" */ '../views/Login.vue'),
        meta: {
          title: 'Login',
        },
      },
    ]
  },
  {
    path: '/',
    component: DefaultLayout,
    meta: {
      hidden: true,
    },
    children: [
      {
        path: '400',
        component: () => import(/* webpackChunkName: "400" */ '../views/errors/400.vue'),
      },
      {
        path: '401',
        component: () => import(/* webpackChunkName: "401" */ '../views/errors/401.vue'),
      },
      {
        path: '403',
        component: () => import(/* webpackChunkName: "403" */ '../views/errors/403.vue'),
      },
      {
        path: '404',
        component: () => import(/* webpackChunkName: "404" */ '../views/errors/404.vue'),
      },
      {
        path: '500',
        component: () => import(/* webpackChunkName: "500" */ '../views/errors/500.vue'),
      },
    ],
  },
];

/**
 * Dynamic Routes
 *
 * These routes are loaded dynamically based on user roles.
 */
export const dynamicRoutes: RouteConfig[] = [
  {
    path: '/account',
    name: 'Account',
    component: AccountLayout,
    redirect: '/account/index',
    meta: {
      requiresAuth: true,
      hidden: true,
      roles: ['user'],
      title: 'My Account',
      icon: 'mdi-account-cog',
    },
    children: [
      {
        path: 'index',
        name: 'AccountIndex',
        component: () => import(/* webpackChunkName: "account/index" */ '../views/account/Index.vue'),
        meta: {
          title: 'Dashboard',
          icon: 'mdi-view-dashboard',
        },
      },
      {
        path: 'profile',
        name: 'AccountProfile',
        component: () => import(/* webpackChunkName: "account/profile" */ '../views/account/Profile.vue'),
        meta: {
          title: 'Profile',
          icon: 'mdi-card-account-details-outline',
        },
      },
      {
        path: 'authorization',
        name: 'AccountAuthorization',
        component: () => import(/* webpackChunkName: "account/authorization" */ '../views/account/Authorization.vue'),
        meta: {
          title: 'Authorization',
          icon: 'mdi-account-lock-outline',
        },
      },
    ]
  },
  adminRoutes,
];

const createRouter = () => new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: constantRoutes,
  scrollBehavior: (to, from, savedPosition) => {
    if (savedPosition) {
      return savedPosition;
    }
    return { x: 0, y: 0 };
  },
});

const router = createRouter();

// Guard setup
router.beforeEach(async (to: Route, from: Route, next: any) => {
  if (AuthModule.loggedIn) {
    if (to.fullPath === '/login') {
      next({ ...from, replace: true });
    } else {
      next();
    }
  } else {
    const result = await AuthModule.CheckAuth();
    if (result) {
      RoutesModule.GenerateRoutes(AuthModule.roles);
      router.addRoutes(RoutesModule.dynamicRoutes);
      next({ ...to, replace: true });
    } else {
      if (RoutesModule.routes.length === 0) {
        RoutesModule.GenerateRoutes([]);
      }
      if (to.matched.some(record => record.meta.requiresAuth)) {
        next({
          path: '/login',
          query: { redirect: to.fullPath }
        });
      } else {
        next();
      }
    }
  }
});

export function resetRouter() {
  const newRouter = createRouter();
  RoutesModule.ClearRoutes();
  (router as any).matcher = (newRouter as any).matcher; // reset router
}

export default router;

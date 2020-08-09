import Vue from 'vue';
import VueRouter, { Route, RouteConfig } from 'vue-router';

import DefaultLayout from '@/layouts/DefaultLayout.vue';
import AuthModule from '@/store/modules/auth';
import PermissionModule from '@/store/modules/permissions';

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
        },
      },
      {
        path: '/about',
        name: 'About',
        component: () => import(/* webpackChunkName: "about" */ '../views/About.vue'),
        meta: {
          title: 'About',
        },
      },
      {
        path: '/login',
        name: 'Login',
        component: () => import(/* webpackChunkName: "login" */ '../views/Login.vue'),
        meta: {
          title: 'Login',
          hidden: true,
        },
      },
    ]
  },
];

/**
 * Dynamic Routes
 *
 * These routes are loaded dynamically based on user roles.
 */
export const dynamicRoutes: RouteConfig[] = [
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
  await AuthModule.CheckAuth();
  if (AuthModule.loggedIn) {
    if (to.fullPath === '/login') {
      next('/');
    } else {
      next();
    }
  } else {
    if (to.matched.some(record => record.meta.requiresAuth)) {
      next({
        path: '/login',
        query: { redirect: to.fullPath }
      });
    } else {
      next();
    }
  }
});

export function resetRouter() {
  const newRouter = createRouter();
  (router as any).matcher = (newRouter as any).matcher; // reset router
}

export default router;

import Vue from 'vue';
import VueRouter, { Route, RouteConfig } from 'vue-router';

import DefaultLayout from '@/layouts/DefaultLayout.vue';
import AuthModule from '@/store/modules/auth';
import RouteModule from '@/store/modules/routes';

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
];

/**
 * Dynamic Routes
 *
 * These routes are loaded dynamically based on user roles.
 */
export const dynamicRoutes: RouteConfig[] = [
  {
    path: '/profile',
    component: DefaultLayout,
    redirect: '/profile/index',
    meta: {
      requiresAuth: true,
      hidden: true,
    },
    children: [
      {
        path: 'index',
        name: 'ProfileIndex',
        component: () => import(/* webpackChunkName: "admin/index" */ '../views/profile/Index.vue'),
        meta: {
          title: 'Profile',
        }
      }
    ]
  }
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
      RouteModule.GenerateRoutes(AuthModule.roles);
      router.addRoutes(RouteModule.dynamicRoutes);
      next({ ...to, replace: true });
    } else {
      if (RouteModule.routes.length === 0) {
        RouteModule.GenerateRoutes([]);
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
  RouteModule.ClearRoutes();
  (router as any).matcher = (newRouter as any).matcher; // reset router
}

export default router;

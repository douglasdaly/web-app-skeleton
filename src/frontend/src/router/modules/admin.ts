import { RouteConfig } from 'vue-router';
import AdminLayout from '@/layouts/AdminLayout.vue';

const adminRoutes: RouteConfig = {
  path: '/admin',
  name: 'Admin',
  component: AdminLayout,
  redirect: '/admin/index',
  meta: {
    requiresAuth: true,
    hidden: true,
    roles: ['admin'],
    title: 'Administration',
    icon: 'mdi-cogs',
  },
  children: [
    {
      path: 'index',
      name: 'AdminIndex',
      component: () => import(/* webpackChunkName: "admin/index" */ '@/views/admin/Index.vue'),
      meta: {
        title: 'Dashboard',
        icon: 'mdi-view-dashboard',
      },
    },
    {
      path: 'users',
      name: 'AdminUsers',
      component: () => import(/* webpackChunkName: "admin/users" */ '@/views/admin/Users.vue'),
      meta: {
        title: 'Users',
        icon: 'mdi-account-multiple',
      },
    },
  ],
};

export default adminRoutes;

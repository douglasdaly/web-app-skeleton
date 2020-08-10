import {
  getModule,
  Module,
  Mutation,
  VuexModule,
  Action,
} from 'vuex-module-decorators';
import { RouteConfig } from 'vue-router';

import { constantRoutes, dynamicRoutes } from '@/router';
import store from '@/store';

/**
 * Checks the given roles and route to see if the roles have
 * permission to access it.
 *
 * @param roles The roles to check against the given route.
 * @param route The route to check.
 */
function hasPermission(roles: string[], route: RouteConfig) {
  if (route.meta && route.meta.roles) {
    return roles.some(role => route.meta.roles.includes(role));
  }
  return true;
}

/**
 * Filters down the given routes to those allowed for the given roles.
 *
 * @param routes The routes to filter for the given roles.
 * @param roles The roles to use for filtering.
 */
export function filterRoutes(routes: RouteConfig[], roles: string[]): RouteConfig[] {
  const ret: RouteConfig[] = []
  routes.forEach(route => {
    const r = { ...route };
    if (hasPermission(roles, r)) {
      if (r.children) {
        r.children = filterRoutes(r.children, roles);
      }
      ret.push(r);
    }
  });
  return ret;
}

@Module({ dynamic: true, name: 'permissions', store })
class RouteModule extends VuexModule {
  public routes: RouteConfig[] = [];
  public dynamicRoutes: RouteConfig[] = [];

  @Mutation
  private SET_ROUTES(routes: RouteConfig[]) {
    this.routes = constantRoutes.concat(routes);
    this.dynamicRoutes = routes;
  }

  @Action
  public GenerateRoutes(roles: string[]) {
    let accessedRoutes: RouteConfig[];
    if (roles.includes('admin')) {
      accessedRoutes = dynamicRoutes;
    } else {
      accessedRoutes = filterRoutes(dynamicRoutes, roles);
    }
    this.SET_ROUTES(accessedRoutes);
  }

  @Action
  public ClearRoutes() {
    this.SET_ROUTES([]);
  }

}

export default getModule(RouteModule);

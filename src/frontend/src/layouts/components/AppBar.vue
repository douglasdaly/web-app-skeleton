<template>
  <!-- App bar -->
  <v-app-bar
    app
    clipped-left
    color="primary"
    dark
  >
    <v-app-bar-nav-icon @click.stop="toggleNavDrawer"></v-app-bar-nav-icon>
    <v-toolbar-title>{{ appTitle }}</v-toolbar-title>
    <v-spacer></v-spacer>

    <v-menu v-if="isLoggedIn"
        bottom
        offset-y
    >
      <template v-slot:activator="{ on, attrs }">
        <v-btn
            icon
            v-bind="attrs"
            v-on="on"
        >
          <v-icon>mdi-account</v-icon>
        </v-btn>
      </template>

      <v-list>
        <v-list-item v-for="(route, idx) in userRoutes"
          :key="`${route.path}-${idx}`"
          :to="route.path"
        >
          <v-list-item-title>{{ route.meta.title }}</v-list-item-title>

          <v-list-item-action v-if="route.meta && route.meta.icon">
            <v-icon dense>{{ route.meta.icon }}</v-icon>
          </v-list-item-action>
        </v-list-item>

        <v-list-item
          link
          @click="logout"
        >
            <v-list-item-title>Logout</v-list-item-title>
            <v-list-item-action>
            <v-icon dense>mdi-account-arrow-right</v-icon>
            </v-list-item-action>
        </v-list-item>
      </v-list>
    </v-menu>
    <v-tooltip v-else
      bottom
    >
      <template v-slot:activator="{ on, attrs }">
        <v-btn
            icon
            :to="{ path: '/login' }"
            v-bind="attrs"
            v-on="on"
        >
          <v-icon>mdi-account-lock</v-icon>
        </v-btn>
      </template>
      <span>Login</span>
    </v-tooltip>
  </v-app-bar>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import { RouteConfig } from 'vue-router';

import AppModule from '@/store/modules/app';
import AuthModule from '@/store/modules/auth';
import RoutesModule from '@/store/modules/routes';

@Component
export default class AppBar extends Vue {
  public loading = false;

  // Computed
  get appTitle(): string {
    return AppModule.appTitle;
  }

  get isLoggedIn(): boolean {
    return AuthModule.loggedIn;
  }

  get userRoutes(): RouteConfig[] {
    const ret: RouteConfig[] = [];
    if (this.isLoggedIn) {
      RoutesModule.dynamicRoutes.forEach((route) => {
        if (route.meta && route.meta.title) {
          ret.push(route);
        }
      });
    }
    return ret;
  }

  // Functions
  public toggleNavDrawer() {
    AppModule.ToggleDrawer();
  }

  public async logout() {
    this.loading = true;
    this.$router.push('/');
    await AuthModule.Logout();
    this.loading = false;
  }

}

</script>

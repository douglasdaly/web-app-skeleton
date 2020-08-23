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
        <v-list-item to="/account/index">
            <v-list-item-title>My Account</v-list-item-title>
            <v-list-item-action>
            <v-icon dense>mdi-account-cog</v-icon>
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

import AppModule from '@/store/modules/app';
import AuthModule from '@/store/modules/auth';

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

  // Functions
  public toggleNavDrawer() {
    AppModule.ToggleDrawer();
  }

  public async logout() {
    this.loading = true;
    await AuthModule.Logout();
    this.loading = false;
    this.$router.push('/');
  }

}

</script>

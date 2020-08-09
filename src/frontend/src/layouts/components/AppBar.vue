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
        <v-list-item>
            <v-list-item-title>Profile</v-list-item-title>
            <v-list-item-action>
            <v-icon dense>mdi-card-account-details-outline</v-icon>
            </v-list-item-action>
        </v-list-item>

        <v-list-item
          link
          @click="logout"
        >
            <v-list-item-title>Logout</v-list-item-title>
            <v-list-item-action>
            <v-icon dense>mdi-account-lock</v-icon>
            </v-list-item-action>
        </v-list-item>
      </v-list>
    </v-menu>
    <v-btn v-else
        icon
        :to="{ path: '/login', query: { redirect: this.$route.fullPath } }"
    >
      <v-icon>mdi-account-lock</v-icon>
    </v-btn>
  </v-app-bar>
</template>

<script lang="ts">
import { Component, Vue, Watch } from 'vue-property-decorator';

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
    const msg = await AuthModule.Logout();
    this.loading = false;
    this.$router.push('/');
  }

}

</script>

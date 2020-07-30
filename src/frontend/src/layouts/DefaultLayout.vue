<template>
  <div>
    <!-- Application bar -->
    <v-app-bar
      app
      color="primary"
      dark
    >
      <v-app-bar-nav-icon @click.stop="drawer = !drawer"></v-app-bar-nav-icon>
      <v-toolbar-title>{{ appName }}</v-toolbar-title>
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

          <v-list-item>
            <v-list-item-title>Logout</v-list-item-title>
            <v-list-item-action>
              <v-icon dense>mdi-account-lock</v-icon>
            </v-list-item-action>
          </v-list-item>
        </v-list>
      </v-menu>
      <v-btn v-else
        icon
        to="/login"
      >
        <v-icon>mdi-account-lock</v-icon>
      </v-btn>
    </v-app-bar>

    <!-- Navigation drawer -->
    <v-navigation-drawer
      v-model="drawer"
      app
    >
      <v-list>
        <v-list-item to="/">
          <v-list-item-action>
            <v-icon>mdi-home</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>Home</v-list-item-title>
          </v-list-item-content>
        </v-list-item>

        <v-list-item to="/about">
          <v-list-item-action>
            <v-icon>mdi-help-box</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>About</v-list-item-title>
          </v-list-item-content>
        </v-list-item>

        <v-list-item @click.stop="left = !left">
          <v-list-item-action>
            <v-icon>mdi-exit-to-app</v-icon>
          </v-list-item-action>
          <v-list-item-content>
            <v-list-item-title>Tools</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>

    <v-navigation-drawer
      v-model="left"
      fixed
      temporary
    >
      <v-list-item>
        <v-list-item-action>
          <v-icon>mdi-briefcase-account-outline</v-icon>
        </v-list-item-action>
        <v-list-item-content>
          <v-list-item-title>Contacts</v-list-item-title>
        </v-list-item-content>
      </v-list-item>

      <v-list-item>
        <v-list-item-action>
          <v-icon>mdi-calendar</v-icon>
        </v-list-item-action>
        <v-list-item-content>
          <v-list-item-title>Calendar</v-list-item-title>
        </v-list-item-content>
      </v-list-item>

      <v-list-item>
        <v-list-item-action>
          <v-icon>mdi-airplane</v-icon>
        </v-list-item-action>
        <v-list-item-content>
          <v-list-item-title>Travel</v-list-item-title>
        </v-list-item-content>
      </v-list-item>
    </v-navigation-drawer>

    <!-- Main content -->
    <v-main>
      <slot />
    </v-main>

    <!-- Footer -->
    <v-footer
      app
      color="secondary"
      dark
    >
      <span>Made with <span class="red--text">❤️</span> by
        <a href="https://github.com/douglasdaly/"
          target="_blank"
          v-text="'Doug'"
        ></a>
      </span>
      <v-spacer></v-spacer>
      <span>&copy; {{ new Date().getFullYear() }}</span>
    </v-footer>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';

import { appName } from '@/env';
import AuthModule from '@/store/modules/auth';

@Component
export default class DefaultLayout extends Vue {
  private appName = appName;
  private drawer = null;
  private left = false;

  get isLoggedIn() {
    return AuthModule.loggedIn;
  }
}
</script>

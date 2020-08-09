<template>
  <div>
    <!-- Navigation -->
    <v-navigation-drawer
      v-model="showNavigation"
      app
      clipped
      disable-resize-watcher
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
  </div>
</template>

<script lang="ts">
import { Component, Vue, Watch } from 'vue-property-decorator';
import { isMobile } from 'mobile-device-detect';

import AppModule, { DeviceType } from '@/store/modules/app';

@Component
export default class NavDrawer extends Vue {
  private left = false;

  // Hooks
  @Watch('$route')
  private onRouteChange() {
    if (AppModule.device == DeviceType.Mobile && this.showNavigation) {
      AppModule.CloseDrawer();
    }
  }

  mounted() {
    if (isMobile) {
      AppModule.ToggleDevice(DeviceType.Mobile);
      AppModule.CloseDrawer();
    }
  }

  // Getters
  get showNavigation() {
    return AppModule.drawer.opened;
  }

  set showNavigation(value: boolean) {
    AppModule.ToggleDrawer(value);
  }

}
</script>

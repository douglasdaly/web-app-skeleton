<template>
  <div>
    <!-- Navigation -->
    <v-navigation-drawer
      v-model="showNavigation"
      app
      clipped
      disable-resize-watcher
    >
      <nav-item v-for="(item, index) in routes"
        :item="item"
        :key="`${item.path}-${index}`"
      ></nav-item>
    </v-navigation-drawer>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Watch } from 'vue-property-decorator';
import { RouteConfig } from 'vue-router';
import { isMobile } from 'mobile-device-detect';

import NavItem from './NavItem.vue';
import AppModule, { DeviceType } from '@/store/modules/app';
import RoutesModule from '@/store/modules/routes';

@Component({
  components: {
    NavItem,
  }
})
export default class NavDrawer extends Vue {

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
  get routes(): RouteConfig[] {
    return RoutesModule.routes;
  }

  get showNavigation() {
    return AppModule.drawer.opened;
  }

  set showNavigation(value: boolean) {
    AppModule.ToggleDrawer(value);
  }

}
</script>

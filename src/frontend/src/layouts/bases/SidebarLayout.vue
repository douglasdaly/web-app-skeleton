<template>
  <default-layout>
    <v-container fluid>
      <v-row>
        <!-- Sidebar -->
        <v-col sm=3 lg=2>
          <sidebar
            :title="title"
            :routes="sidebarRoutes"
          ></sidebar>
        </v-col>

        <!-- Content -->
        <v-col>
          <slot>
            <router-view></router-view>
          </slot>
        </v-col>
      </v-row>
    </v-container>
  </default-layout>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import { RouteConfig } from 'vue-router';

import RoutesModule from '@/store/modules/routes';

import DefaultLayout from '../DefaultLayout.vue';
import Sidebar from '../components/Sidebar.vue';

@Component({
  components: {
    DefaultLayout,
    Sidebar,
  }
})
export default class SidebarLayout extends Vue {
  protected title?: string;
  protected parentPath?: string;

  // Computed
  get sidebarRoutes() {
    const ret: RouteConfig[] = [];
    if (this.parentPath) {
      RoutesModule.dynamicRoutes.forEach(route => {
        if (route.path === this.parentPath) {
          if (route.children) {
            ret.push(...route.children);
          }
        }
      });
    }
    return ret;
  }

}
</script>

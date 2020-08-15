<template>
  <default-layout>
    <v-container fluid>
      <v-row>
        <!-- Sidebar -->
        <v-col sm=3 lg=2>
          <sidebar
            title="My Account"
            :routes="accountRoutes"
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

import DefaultLayout from './DefaultLayout.vue';
import Sidebar from './components/Sidebar.vue';

@Component({
  name: 'AccountLayout',
  components: {
    DefaultLayout,
    Sidebar,
  }
})
export default class AccountLayout extends Vue {

  // Computed
  get accountRoutes() {
    const ret: RouteConfig[] = [];
    RoutesModule.dynamicRoutes.forEach(route => {
      if (route.path === '/account') {
        if (route.children) {
          ret.push(...route.children);
        }
      }
    });
    return ret;
  }

}
</script>

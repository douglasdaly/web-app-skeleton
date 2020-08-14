<template>
  <v-card dark color="secondary">
    <v-list-item>
      <v-list-item-content>
        <v-list-item-title
          class="headline-2"
        >
          My Account
        </v-list-item-title>
      </v-list-item-content>
    </v-list-item>

    <v-divider></v-divider>

    <v-list dense light>
      <v-list-item v-for="(route, key) in accountRoutes"
        :key="`${route.name}-${key}`"
        :to="route.path"
      >
        <v-list-item-icon>
          <v-icon v-if="route.meta && route.meta.icon">
            {{ route.meta.icon }}
          </v-icon>
        </v-list-item-icon>

        <v-list-item-content>
          <v-list-item-title v-if="route.meta && route.meta.title">
            {{ route.meta.title }}
          </v-list-item-title>
        </v-list-item-content>
      </v-list-item>
    </v-list>
  </v-card>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import { RouteConfig } from 'vue-router';

import RoutesModule from '@/store/modules/routes';

@Component
export default class Sidebar extends Vue {

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

};
</script>

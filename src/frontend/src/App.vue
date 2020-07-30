<template>
  <v-app>
    <component :is="this.layout">
      <router-view />
    </component>
  </v-app>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';

import DefaultLayout from './layouts/DefaultLayout.vue';

@Component
export default class App extends Vue {
  get layout() {
    return this.$route.meta.layout || DefaultLayout;
  }
}
</script>

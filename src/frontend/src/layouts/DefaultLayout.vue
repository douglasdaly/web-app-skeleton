<template>
  <v-app>

    <!-- Navigation -->
    <nav-drawer></nav-drawer>

    <!-- App bar -->
    <app-bar></app-bar>

    <!-- Main content -->
    <app-main>
      <slot></slot>
    </app-main>

    <!-- Footer -->
    <footer-bar></footer-bar>

  </v-app>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';

import AppBar from './components/AppBar.vue';
import AppMain from './components/AppMain.vue';
import FooterBar from './components/FooterBar.vue';
import NavDrawer from './components/NavDrawer.vue';

@Component({
  name: 'DefaultLayout',
  components: {
    AppBar,
    AppMain,
    FooterBar,
    NavDrawer,
  }
})
export default class DefaultLayout extends Vue {
}
</script>

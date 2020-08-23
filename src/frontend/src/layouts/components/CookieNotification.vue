<template>
  <v-snackbar
    v-model="show"
    dark
    timeout=-1
  >
    <v-icon
      class="mr-2"
      icon="mdi-cookie"
      color="warning"
      size=35
    >
      mdi-cookie
    </v-icon>

    <span class="subtitle-2">
      This website uses cookies for necessary functionality.
    </span>

    <template v-slot:action>
      <v-btn
        class="mr-2"
        color="success"
        @click="accept()"
        small
      >
        Got it!
      </v-btn>
    </template>
  </v-snackbar>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';

import AppModule from '@/store/modules/app';

@Component
export default class CookieNotification extends Vue {

  // Computed
  get show() {
    return AppModule.cookieNotify;
  }

  // Methods
  public async accept() {
    await AppModule.CookiesNotified();
  }

}
</script>

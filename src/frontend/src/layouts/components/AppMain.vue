<template>
  <v-main>
    <slot>
      <router-view />
    </slot>
  </v-main>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';

@Component
export default class AppMain extends Vue {
}
</script>

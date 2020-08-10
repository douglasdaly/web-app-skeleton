<template>
  <v-container>
    <HelloWorld msg="Welcome to Your Vue.js App"/>
  </v-container>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';

import HelloWorld from '@/components/HelloWorld.vue';

@Component({
  components: {
    HelloWorld,
  }
})
export default class Home extends Vue {
};
</script>

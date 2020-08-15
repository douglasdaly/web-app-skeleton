<template>
  <v-card
    flat
  >
    <v-list-item>
      <v-list-item-content>
        <v-list-item-title
          class="headline"
        >
          Dashboard
        </v-list-item-title>
        <v-list-item-subtitle>
          Your personalized dashboard
        </v-list-item-subtitle>
      </v-list-item-content>
    </v-list-item>

    <v-divider></v-divider>

    <!-- Content -->

  </v-card>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';

@Component({
  name: 'AccountIndex',
})
export default class AccountIndex extends Vue {
};
</script>

<template>
  <v-container fluid>
    <v-row>
      <v-col>
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

        </v-card>
      </v-col>

      <!-- Sidebar -->
      <v-col sm="3" lg="2">
        <sidebar></sidebar>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';

import Sidebar from './components/Sidebar.vue';

@Component({
  components: {
    Sidebar,
  }
})
export default class AccountIndex extends Vue {
};
</script>

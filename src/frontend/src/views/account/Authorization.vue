<template>
  <v-container>
    <v-row>
      <v-col cols="3">
        <sidebar></sidebar>
      </v-col>
      <v-col>
        <v-card flat>
          <v-list-item>
            <v-list-item-content>
              <v-list-item-title
                class="headline"
              >
                Authorization
              </v-list-item-title>
              <v-list-item-subtitle>
                Login credentials management
              </v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>

          <v-divider></v-divider>

        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';

import AuthModule from '@/store/modules/auth';
import Sidebar from './components/Sidebar.vue';

@Component({
  components: {
    Sidebar,
  }
})
export default class AccountAuthorization extends Vue {

  // Computed
  get user() {
    return AuthModule.user;
  }

}
</script>

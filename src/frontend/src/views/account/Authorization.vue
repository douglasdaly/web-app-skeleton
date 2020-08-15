<template>
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

    <!-- Content -->
    <display-user-auth v-model="user"
      show-roles
    ></display-user-auth>

  </v-card>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';

import AuthModule from '@/store/modules/auth';

import DisplayUserAuth from '@/components/auth/DisplayUserAuth.vue';

@Component({
  name: 'AccountAuthorization',
  components: {
    DisplayUserAuth,
  }
})
export default class AccountAuthorization extends Vue {

  // Computed
  get user() {
    return AuthModule.user;
  }

}
</script>

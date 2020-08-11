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
                My Profile
              </v-list-item-title>
              <v-list-item-subtitle>
                Your profile information
              </v-list-item-subtitle>
            </v-list-item-content>
            <v-list-item-avatar>
              <v-tooltip
                bottom
                v-if="!modify"
              >
                <template v-slot:activator="{ on, attrs }">
                  <v-btn
                    icon
                    color="primary"
                    v-bind="attrs"
                    v-on="on"
                    @click="beginChanges"
                  >
                    <v-icon>mdi-pencil</v-icon>
                  </v-btn>
                </template>
                <span>Modify</span>
              </v-tooltip>
              <v-tooltip
                bottom
                v-if="modify"
              >
                <template v-slot:activator="{ on, attrs }">
                  <v-btn
                    icon
                    color="success"
                    v-bind="attrs"
                    v-on="on"
                    @click="saveChanges"
                  >
                    <v-icon>mdi-checkbox-marked-circle</v-icon>
                  </v-btn>
                </template>
                <span>Save</span>
              </v-tooltip>
            </v-list-item-avatar>
          </v-list-item>

          <v-divider></v-divider>

          <display-user :user="user"></display-user>

        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';

import AuthModule from '@/store/modules/auth';
import Sidebar from './components/Sidebar.vue';
import DisplayUser from '@/components/users/DisplayUser.vue';

@Component({
  components: {
    DisplayUser,
    Sidebar,
  }
})
export default class AccountProfile extends Vue {
  private modify = false;

  // Computed
  get user() {
    return AuthModule.user;
  }

  // Functions
  private beginChanges() {
    this.modify = true;
  }

  private saveChanges() {
    this.modify = false;
  }

};
</script>

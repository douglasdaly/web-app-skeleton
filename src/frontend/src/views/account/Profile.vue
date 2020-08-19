<template>
  <v-card flat
    :loading="loading"
  >
    <v-list-item>
      <v-list-item-content>
        <v-list-item-title
          class="headline"
        >
          Profile
        </v-list-item-title>
        <v-list-item-subtitle>
          Your profile information
        </v-list-item-subtitle>
      </v-list-item-content>
      <v-list-item-avatar v-if="!modify">
        <v-tooltip
          bottom
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
      </v-list-item-avatar>
      <template v-else>
        <v-list-item-avatar>
          <v-tooltip
            bottom
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
        <v-list-item-avatar>
          <v-tooltip
            bottom
          >
            <template v-slot:activator="{ on, attrs }">
              <v-btn
                icon
                color="error"
                v-bind="attrs"
                v-on="on"
                @click="cancelChanges"
              >
                <v-icon>mdi-close-circle</v-icon>
              </v-btn>
            </template>
            <span>Cancel</span>
          </v-tooltip>
        </v-list-item-avatar>
      </template>
    </v-list-item>

    <v-divider></v-divider>

    <!-- Content -->
    <display-user v-if="!modify"
      v-model="user"
    ></display-user>
    <edit-user v-else
      v-model="user"
      ref="form"
    ></edit-user>

  </v-card>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';

import AuthModule from '@/store/modules/auth';
import DisplayUser from '@/components/users/DisplayUser.vue';
import EditUser from '@/components/users/EditUser.vue';

@Component({
  name: "AccountProfile",
  components: {
    DisplayUser,
    EditUser,
  },
})
export default class AccountProfile extends Vue {
  private loading = false;
  private modify = false;

  // Computed
  get user() {
    return AuthModule.user;
  }

  // Functions
  private beginChanges() {
    this.modify = true;
  }

  private async saveChanges() {
    this.modify = false;
    this.loading = true;
    if ((this.$refs.form as EditUser).validate())
    {
      await (this.$refs.form as EditUser).submit();
      await AuthModule.GetUserInfo();
    }
    this.loading = false;
  }

  private cancelChanges() {
    this.modify = false;
  }

};
</script>

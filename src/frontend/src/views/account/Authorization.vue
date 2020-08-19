<template>
  <v-card flat
    :loading="loading"
  >
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
    <display-user-auth v-if="!modify"
      v-model="user"
      show-roles
    ></display-user-auth>
    <template v-else>
      <v-form
        ref="form"
        v-model="valid"
      >
        <v-container fluid>
          <v-row>
            <v-col>
              <v-text-field
                v-model="password"
                :rules="passwordRules"
                label="Current Password"
                required
              ></v-text-field>
            </v-col>
          </v-row>
        </v-container>
      </v-form>

      <edit-user-auth
        ref="authForm"
        v-model="authUpdate"
      ></edit-user-auth>

      <div v-if="errorMsg">
        <v-alert
          transition="fade-transition"
          type="error"
        >
          {{ errorMsg }}
        </v-alert>
      </div>
    </template>

  </v-card>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';

import api from '@/api';
import AuthModule from '@/store/modules/auth';

import DisplayUserAuth from '@/components/auth/DisplayUserAuth.vue';
import EditUserAuth, { UserAuthUpdate } from '@/components/auth/EditUserAuth.vue';

@Component({
  name: 'AccountAuthorization',
  components: {
    DisplayUserAuth,
    EditUserAuth,
  }
})
export default class AccountAuthorization extends Vue {
  private loading = false;
  private modify = false;

  private valid = false;
  private password = '';
  private authUpdate: UserAuthUpdate = {
    newEmail: '',
    newPassword: '',
  };
  private errorMsg: string | null = null;

  // Computed
  get user() {
    return AuthModule.user;
  }

  get passwordRules () {
    return [
      (v: string) => !!v || 'Current password required',
    ];
  }

  // Functions
  public validate() {
    (this.$refs.authForm as EditUserAuth).validate();
    return this.valid && (this.$refs.authForm as EditUserAuth).valid;
  }

  private beginChanges() {
    this.errorMsg = null;
    this.password = '';
    this.authUpdate.newEmail = this.user ? this.user.email : '';
    this.authUpdate.newPassword = '';
    this.modify = true;
  }

  private async saveChanges() {
    this.loading = true;
    this.errorMsg = null;
    if (this.validate())
    {
      const result = await api.auth.updateLoginMe(
        this.password,
        this.authUpdate.newEmail !== '' ? this.authUpdate.newEmail : undefined,
        this.authUpdate.newPassword !== '' ? this.authUpdate.newPassword : undefined,
      )
        .then(() => {
          this.errorMsg = null;
          return true;
        })
        .catch(res => {
          this.errorMsg = res.response.data.detail;
          return false;
        });
      if (result) {
        await AuthModule.GetUserInfo();
        this.modify = false;
      }
    }
    this.loading = false;
  }

  private cancelChanges() {
    this.errorMsg = null;
    this.password = '';
    this.modify = false;
  }

}
</script>

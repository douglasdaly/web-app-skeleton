<template>
  <v-card
    :loading="loading"
  >
    <!-- Title -->
    <v-list-item>
      <v-list-item-content>
        <v-list-item-title class="headline">
          Edit User
        </v-list-item-title>
      </v-list-item-content>

      <v-spacer></v-spacer>

      <v-list-item-action>
        <v-btn
          icon
          dark
          color="error"
          @click="cancel()"
        >
          <v-icon>mdi-close</v-icon>
        </v-btn>
      </v-list-item-action>
    </v-list-item>

    <v-divider class="pb-1"></v-divider>

    <!-- Content -->
    <v-expansion-panels
      accordion
      v-model="openPanel"
    >
      <!-- Credentials -->
      <v-expansion-panel v-if="editLogin">
        <v-expansion-panel-header
          class="subtitle-1 primary--text"
        >
          Login
        </v-expansion-panel-header>
        <v-expansion-panel-content>
          <edit-user-credentials
            ref="loginForm"
            v-model="loginUpdate"
            is-child
            @submit="submit()"
            @cancel="$emit('cancel')"
          ></edit-user-credentials>
        </v-expansion-panel-content>
      </v-expansion-panel>

      <!-- Authorization -->
      <v-expansion-panel v-if="editAuths">
        <v-expansion-panel-header
          class="subtitle-1 primary--text"
        >
          Authorizations
        </v-expansion-panel-header>
        <v-expansion-panel-content>
          <modify-user-permissions
            ref="authForm"
            v-model="userUpdate"
            is-child
            @submit="submit()"
            @cancel="$emit('cancel')"
          ></modify-user-permissions>
        </v-expansion-panel-content>
      </v-expansion-panel>

      <!-- Name -->
      <v-expansion-panel>
        <v-expansion-panel-header
          class="subtitle-1 primary--text"
        >
          Name
        </v-expansion-panel-header>
        <v-expansion-panel-content>
          <edit-name
            ref="nameForm"
            v-model="userUpdate.name"
            is-child
            @submit="submit()"
            @cancel="$emit('cancel')"
          ></edit-name>
        </v-expansion-panel-content>
      </v-expansion-panel>

    </v-expansion-panels>

    <!-- Card actions -->
    <v-card-actions>
      <v-btn
        color="error"
        tabindex="-1"
        @click="cancel()"
      >
        Cancel
      </v-btn>

      <v-spacer></v-spacer>

      <v-btn
        color="success"
        :loading="loading"
        @click="submit()"
      >
        Edit User
      </v-btn>
    </v-card-actions>

  </v-card>
</template>

<script lang="ts">
import { Component, Model, Prop, Vue } from 'vue-property-decorator';

import api from '@/api';
import { IUser, INameUpdate, IRole, IUserUpdate } from '@/api/schema';
import EditName from '@/components/names/EditName.vue';
import EditUserCredentials, { UserCredentialsUpdate } from '@/components/auth/EditUserCredentials.vue';
import ModifyUserPermissions from '@/components/auth/ModifyUserPermissions.vue';

function createBlankUpdate(userIn: IUser): IUserUpdate {
  return {
    email: userIn.email,
    name: userIn.name ? userIn.name : Object(),
    roles: userIn.roles.map((role: IRole): string => role.name.toLowerCase()),
    isActive: userIn.isActive,
    isSuperuser: userIn.isSuperuser,
    isAdmin: userIn.isAdmin,
  };
};

@Component({
  components: {
    EditName,
    EditUserCredentials,
    ModifyUserPermissions,
  },
})
export default class EditUserFull extends Vue {
  @Model('change') private user!: IUser;
  @Prop([Boolean]) private isChild?: boolean;
  @Prop([Boolean]) private editLogin?: boolean;
  @Prop([Boolean]) private editAuths?: boolean;

  private openPanel = 0;
  private loading = false;
  private valid = false;
  private loginUpdate: UserCredentialsUpdate = {
    newEmail: this.user.email ? this.user.email : '',
    newPassword: '',
  };
  private userUpdate: IUserUpdate = createBlankUpdate(this.user);

  // Methods
  public validate() {
    let ret = true;
    if (this.$refs.authForm) {
      ret = ret && (this.$refs.authForm as ModifyUserPermissions).valid;
    }
    if (this.$refs.loginForm) {
      ret = ret && (this.$refs.loginForm as EditUserCredentials).valid;
    }
    if (this.$refs.nameForm) {
      ret = ret && (this.$refs.nameForm as EditName).valid;
    }
    this.valid = ret;
    return ret;
  }

  public reset() {
    this.openPanel = 0;
    this.valid = false;
    this.loginUpdate.newEmail = this.user.email ? this.user.email : '';
    this.loginUpdate.newPassword = '';
  }

  public async submit(isChild?: boolean) {
    this.loading = true;
    const child = isChild === false ? false : this.isChild;
    if (child) {
      this.$emit('submit');
    } else {
      if (!!child || this.validate()) {
        if (this.loginUpdate.newEmail !== '') {
          this.userUpdate.email = this.loginUpdate.newEmail;
        }
        if (this.loginUpdate.newPassword !== '') {
          this.userUpdate.password = this.loginUpdate.newPassword;
        }
        const newUser = await api.user.updateUser(this.user.uid, this.userUpdate);
        this.userUpdate = createBlankUpdate(newUser);
      }
      this.$emit('submit');
    }
    this.reset();
    this.loading = false;
  }

  public cancel() {
    this.reset();
    this.$emit('cancel');
  }

}
</script>

<template>
  <v-form
    ref="form"
    v-model="valid"
  >
    <v-container fluid>
      <!-- User Flags -->
      <v-row>
        <v-col cols="auto">
          <span>User Flags:</span>
        </v-col>
        <v-col>
          <v-row>
            <v-col>
              <v-switch
                v-model="user.isActive"
                label="Is Active?"
                prepend-icon="mdi-account-voice"
              ></v-switch>
            </v-col>
            <v-col>
              <v-switch v-model="user.isSuperuser"
                label="Is Power User?"
                prepend-icon="mdi-shield-account-outline"
              ></v-switch>
            </v-col>
            <v-col>
              <v-switch v-model="user.isAdmin"
                label="Is Administrator?"
                prepend-icon="mdi-shield-star"
              ></v-switch>
            </v-col>
          </v-row>
        </v-col>
      </v-row>

      <!-- Roles -->
      <v-row>
        <v-col>
          <v-select
            ref="rolesSelect"
            v-model="user.roles"
            :loading="loading"
            :items="roles"
            item-text="name"
            item-value="name"
            label="Role(s)"
            multiple
            hint="Select the role(s) for the new user"
            persistent-hint
          ></v-select>
        </v-col>
      </v-row>
    </v-container>
  </v-form>
</template>

<script lang="ts">
import { Component, Model, Prop, Vue } from 'vue-property-decorator';

import api from '@/api';
import { IRole, IUserCreate, IUserUpdate } from '@/api/schema';

@Component
export default class ModifyUserPermissions extends Vue {
  @Model('change') private user!: IUserCreate | IUserUpdate;
  @Prop([Boolean]) private isChild?: boolean;

  public valid = false;
  private loading = false;

  private roles: IRole[] = [];

  // Hooks
  async mounted() {
    if (!this.user.roles) {
      this.user.roles = [];
    }
    await this.fetchRoles();
  }

  // Functions
  public async fetchRoles() {
    this.loading = true;
    this.roles = [];
    const allRoles = await api.roles.readRoles()
    this.roles.push(...allRoles);
    this.loading = false;
  }

  // - Form
  public focus() {
    this.$nextTick(() => {
      (this.$refs.rolesSelect as HTMLFormElement).focus();
    });
  }

  public validate() {
    this.valid = (this.$refs.form as HTMLFormElement).validate();
    return this.valid;
  }

  public reset() {
    (this.$refs.form as HTMLFormElement).reset();
    this.loading = false;
    this.roles = [];
    this.valid = false;
  }

  public submit(isChild?: boolean) {
    const child = isChild === false ? false : this.isChild;
    if (child) {
      this.$emit('submit');
    }
  }

}
</script>

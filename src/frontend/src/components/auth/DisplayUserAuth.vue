<template>
  <v-list two-line>
    <!-- Email -->
    <v-list-item>
      <v-list-item-icon>
        <v-icon>mdi-email</v-icon>
      </v-list-item-icon>

      <v-list-item-content>
        <v-list-item-title>{{ user.email }}</v-list-item-title>
        <v-list-item-subtitle>Email</v-list-item-subtitle>
      </v-list-item-content>
    </v-list-item>

    <!-- Roles -->
    <v-list-item v-if="showRoles && roleString">
      <v-list-item-icon>
        <v-icon>mdi-account-key</v-icon>
      </v-list-item-icon>

      <v-list-item-content>
        <v-list-item-title>{{ roleString }}</v-list-item-title>
        <v-list-item-subtitle>{{ roleTitle }}</v-list-item-subtitle>
      </v-list-item-content>
    </v-list-item>
  </v-list>
</template>

<script lang="ts">
import { Component, Model, Prop, Vue } from 'vue-property-decorator';

import { IUser } from '@/api/schema/user';

@Component
export default class DisplayUserAuth extends Vue {
  @Model('change') private user!: IUser;
  @Prop([Boolean]) readonly showRoles?: boolean;

  // Computed
  get roleString() {
    if (this.user.roles) {
      const dispRoles: string[] = [];
      this.user.roles.forEach(role => {
        const roleName = role.name;
        dispRoles.push(roleName.charAt(0).toUpperCase() + roleName.slice(1));
      });
      return dispRoles.join(', ');
    }
  }

  get roleTitle(): string {
    if (this.user.roles.length > 1) {
      return 'Roles';
    }
    return 'Role';
  }

}
</script>

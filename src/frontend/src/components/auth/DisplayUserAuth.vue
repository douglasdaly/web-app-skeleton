<template>
  <v-list two-line>
    <!-- GUID -->
    <v-list-item v-if="showUid && user.uid">
      <v-list-item-icon>
        <v-icon>mdi-numeric</v-icon>
      </v-list-item-icon>

      <v-list-item-content>
        <v-list-item-title class="overline">{{ user.uid }}</v-list-item-title>
        <v-list-item-subtitle>Unique ID</v-list-item-subtitle>
      </v-list-item-content>
    </v-list-item>

    <!-- Email -->
    <v-list-item v-if="showEmail && user.email">
      <v-list-item-icon>
        <v-icon>mdi-email</v-icon>
      </v-list-item-icon>

      <v-list-item-content>
        <v-list-item-title>{{ user.email }}</v-list-item-title>
        <v-list-item-subtitle>Email</v-list-item-subtitle>
      </v-list-item-content>
    </v-list-item>

    <!-- Permission Flags: Active -->
    <v-list-item v-if="showFlags && user.isActive !== undefined">
      <v-list-item-icon>
        <v-icon>mdi-account-voice</v-icon>
      </v-list-item-icon>

      <v-list-item-content>
        <v-list-item-title>
          <v-icon v-if="user.isActive" color="success">mdi-check</v-icon>
          <v-icon v-else color="error">mdi-close</v-icon>
        </v-list-item-title>
        <v-list-item-subtitle>Is an Active User?</v-list-item-subtitle>
      </v-list-item-content>
    </v-list-item>

    <!-- Permission Flags: Superuser -->
    <v-list-item v-if="showFlags && user.isSuperuser !== undefined">
      <v-list-item-icon>
        <v-icon>mdi-shield-account-outline</v-icon>
      </v-list-item-icon>

      <v-list-item-content>
        <v-list-item-title>
          <v-icon v-if="user.isSuperuser" color="success">mdi-check</v-icon>
          <v-icon v-else color="error">mdi-close</v-icon>
        </v-list-item-title>
        <v-list-item-subtitle>Is a Power User?</v-list-item-subtitle>
      </v-list-item-content>
    </v-list-item>

    <!-- Permission Flags: Admin -->
    <v-list-item v-if="showFlags && user.isAdmin !== undefined">
      <v-list-item-icon>
        <v-icon>mdi-shield-star</v-icon>
      </v-list-item-icon>

      <v-list-item-content>
        <v-list-item-title>
          <v-icon v-if="user.isAdmin" color="success">mdi-check</v-icon>
          <v-icon v-else color="error">mdi-close</v-icon>
        </v-list-item-title>
        <v-list-item-subtitle>Is an Administrator?</v-list-item-subtitle>
      </v-list-item-content>
    </v-list-item>

    <!-- Roles -->
    <v-list-item v-if="showRoles">
      <v-list-item-icon>
        <v-icon>mdi-account-key</v-icon>
      </v-list-item-icon>

      <v-list-item-content>
        <v-list-item-title v-if="roleString">
          {{ roleString }}
        </v-list-item-title>
        <v-list-item-title v-else>
          <i color="gray">&lt;None&gt;</i>
        </v-list-item-title>
        <v-list-item-subtitle>{{ roleTitle }}</v-list-item-subtitle>
      </v-list-item-content>
    </v-list-item>
  </v-list>
</template>

<script lang="ts">
import { Component, Model, Prop, Vue } from 'vue-property-decorator';

import { IRole, IUser, IUserCreate, IUserUpdate } from '@/api/schema';

@Component
export default class DisplayUserAuth extends Vue {
  @Model('change') private user!: IUser | IUserCreate | IUserUpdate;
  @Prop([Boolean]) private showRoles?: boolean;
  @Prop([Boolean]) private showUid?: boolean;
  @Prop([Boolean]) private showFlags?: boolean;
  @Prop({ default: true }) private showEmail!: boolean;

  // Computed
  get roleString() {
    if (this.user.roles) {
      const dispRoles: string[] = [];
      this.user.roles.forEach((role: IRole | string) => {
        let roleName;
        if (typeof role === 'string') {
          roleName = role;
        } else {
          roleName = role.name;
        }
        dispRoles.push(roleName.charAt(0).toUpperCase() + roleName.slice(1));
      });
      return dispRoles.join(', ');
    }
  }

  get roleTitle(): string {
    if (this.user.roles && this.user.roles.length > 1) {
      return 'Roles';
    }
    return 'Role';
  }

}
</script>

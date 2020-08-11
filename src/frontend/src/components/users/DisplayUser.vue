<template>
  <v-list two-line>
    <!-- Name -->
    <v-list-item v-if="user.name && user.name.title">
      <v-list-item-avatar>
        <v-icon>
          mdi-account
        </v-icon>
      </v-list-item-avatar>

      <v-list-item-content>
        <v-list-item-title>{{ user.name.title }}</v-list-item-title>
        <v-list-item-subtitle>Title</v-list-item-subtitle>
      </v-list-item-content>
    </v-list-item>

    <v-list-item>
      <v-list-item-avatar>
        <v-icon v-if="!user.name || !user.name.title">
          mdi-account
        </v-icon>
      </v-list-item-avatar>

      <v-list-item-content>
        <v-list-item-title v-if="user.name">
          {{ user.name.first }}
        </v-list-item-title>
        <v-list-item-title v-else
          class="grey--text"
        >
          &lt;Not Set&gt;
        </v-list-item-title>
        <v-list-item-subtitle>First Name</v-list-item-subtitle>
      </v-list-item-content>
    </v-list-item>

    <v-list-item v-if="user.name && user.name.middle">
      <v-list-item-avatar></v-list-item-avatar>

      <v-list-item-content>
        <v-list-item-title>{{ user.name.middle }}</v-list-item-title>
        <v-list-item-subtitle>Middle Name</v-list-item-subtitle>
      </v-list-item-content>
    </v-list-item>

    <v-list-item>
      <v-list-item-avatar></v-list-item-avatar>

      <v-list-item-content>
        <v-list-item-title v-if="user.name">
          {{ user.name.last }}
        </v-list-item-title>
        <v-list-item-title v-else
          class="grey--text"
        >
          &lt;Not Set&gt;
        </v-list-item-title>
        <v-list-item-subtitle>Last Name</v-list-item-subtitle>
      </v-list-item-content>
    </v-list-item>

    <v-list-item v-if="user.name && user.name.suffix">
      <v-list-item-avatar></v-list-item-avatar>

      <v-list-item-title>
        {{ user.name.suffix }}
      </v-list-item-title>
      <v-list-item-subtitle>Suffix</v-list-item-subtitle>
    </v-list-item>

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
  </v-list>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';

import { IUser } from '@/api/schema';

@Component
export default class DisplayUser extends Vue {
  @Prop({ required: true }) private user!: IUser;
};
</script>

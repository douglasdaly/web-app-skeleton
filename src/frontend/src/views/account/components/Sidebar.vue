<template>
  <v-card dark color="secondary">
    <v-list-item>
      <v-list-item-content>
        <v-list-item-title
          class="headline-2"
        >
          My Account
        </v-list-item-title>
      </v-list-item-content>
    </v-list-item>

    <v-divider></v-divider>

    <v-list dense light>
      <v-list-item to="index">
        <v-list-item-icon>
          <v-icon>mdi-view-dashboard</v-icon>
        </v-list-item-icon>

        <v-list-item-content>
          <v-list-item-title>Dashboard</v-list-item-title>
        </v-list-item-content>
      </v-list-item>

      <v-list-item to="profile">
        <v-list-item-icon>
          <v-icon>mdi-card-account-details-outline</v-icon>
        </v-list-item-icon>

        <v-list-item-content>
          <v-list-item-title>Profile</v-list-item-title>
        </v-list-item-content>
      </v-list-item>

      <v-list-item to="authorization">
        <v-list-item-icon>
          <v-icon>mdi-account-lock-outline</v-icon>
        </v-list-item-icon>

        <v-list-item-content>
          <v-list-item-title>Authorization</v-list-item-title>
        </v-list-item-content>
      </v-list-item>
    </v-list>
  </v-card>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';

@Component
export default class Sidebar extends Vue {
};
</script>

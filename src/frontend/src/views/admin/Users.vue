<template>
  <v-card
    flat
  >
    <v-list-item>
      <v-list-item-content>
        <v-list-item-title
          class="headline"
        >
          Users
        </v-list-item-title>
        <v-list-item-subtitle>
          User management tools.
        </v-list-item-subtitle>
      </v-list-item-content>
    </v-list-item>

    <v-divider></v-divider>

    <!-- Content -->

    <users-table></users-table>

  </v-card>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';

import UsersTable from '@/components/users/UsersTable.vue';

@Component({
  name: 'AdminUsers',
  components: {
    UsersTable,
  }
})
export default class AdminUsers extends Vue {
};
</script>

<template>
  <div>
    <!-- Name -->
    <display-name
      v-model="user.name"
      :showIcons="showIcons"
    ></display-name>

    <v-list two-line>
      <!-- Email -->
      <v-list-item v-if="showEmail">
        <v-list-item-icon v-if="showIcons">
          <v-icon>mdi-email</v-icon>
        </v-list-item-icon>

        <v-list-item-content>
          <v-list-item-title>{{ user.email }}</v-list-item-title>
          <v-list-item-subtitle>Email</v-list-item-subtitle>
        </v-list-item-content>
      </v-list-item>
    </v-list>
  </div>
</template>

<script lang="ts">
import { Component, Model, Prop, Vue } from 'vue-property-decorator';

import { IUser } from '@/api/schema';
import DisplayName from '@/components/names/DisplayName.vue';

@Component({
  components: {
    DisplayName,
  }
})
export default class DisplayUser extends Vue {
  @Model('change') private user!: IUser;
  @Prop({ default: false }) private showEmail!: boolean;
  @Prop({ default: true }) private showIcons!: boolean;
};
</script>

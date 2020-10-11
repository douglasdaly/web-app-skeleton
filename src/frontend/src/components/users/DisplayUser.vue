<template>
  <div>
    <!-- Name -->
    <display-name
      v-model="user.name"
      :showIcons="showIcons"
    ></display-name>

    <!-- Email/Roles -->
    <display-user-auth v-if="showEmail || showRoles"
      v-model="user"
      :show-email="showEmail"
      :show-roles="showRoles"
    ></display-user-auth>

  </div>
</template>

<script lang="ts">
import { Component, Model, Prop, Vue } from 'vue-property-decorator';

import { IUser } from '@/api/schema';
import DisplayUserAuth from '@/components/auth/DisplayUserAuth.vue';
import DisplayName from '@/components/names/DisplayName.vue';

@Component({
  components: {
    DisplayName,
    DisplayUserAuth,
  }
})
export default class DisplayUser extends Vue {
  @Model('change') private user!: IUser;
  @Prop({ default: true }) private showEmail!: boolean;
  @Prop([Boolean]) private showRoles?: boolean;
  @Prop({ default: true }) private showIcons!: boolean;
};
</script>

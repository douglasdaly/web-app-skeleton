<template>
  <v-card
    :dark="dark"
  >
    <v-card-title v-if="title"
      class="headline"
    >
      {{ title }}
    </v-card-title>

    <v-divider v-if="title"></v-divider>

    <v-container v-if="user"
      class="pt-0"
    >
      <v-row>
        <v-col class="pt-0">
          <display-user-auth
            v-model="user"
            show-uid
            :show-email="false"
            class="py-0"
          ></display-user-auth>
        </v-col>
      </v-row>

      <v-row class="pt-0">
        <v-col cols="auto" class="pt-0">
          <display-user-auth
            v-model="user"
            show-flags
            show-roles
            class="py-0"
          ></display-user-auth>
        </v-col>

        <v-col class="pt-0">
          <display-user
            v-model="user"
            :show-email="false"
            class="py-0"
          ></display-user>
        </v-col>
      </v-row>
    </v-container>

    <v-card-actions v-if="showActions">
      <v-spacer></v-spacer>

      <v-btn
        color="secondary"
        @click="$emit('cancel')"
      >
        Close
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script lang="ts">
import { Component, Model, Prop, Vue } from 'vue-property-decorator';

import api from '@/api';
import { IUser, IUserCreate, IUserUpdate } from '@/api/schema';

import DisplayUser from '@/components/users/DisplayUser.vue';
import DisplayUserAuth from '@/components/auth/DisplayUserAuth.vue';

@Component({
  components: {
    DisplayUser,
    DisplayUserAuth,
  }
})
export default class DisplayUserDetailed extends Vue {
  @Model('change') private user!: IUser | IUserCreate | IUserUpdate;
  @Prop([Boolean]) private dark?: boolean;
  @Prop([Boolean]) private showActions?: boolean;
  @Prop({ default: 'User Details' }) private title!: string;
}
</script>

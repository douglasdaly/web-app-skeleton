<template>
  <v-card
    :dark="dark"
  >
    <slot name="title">
      <v-card-title v-if="showTitle"
        class="headline"
      >
        {{ title }}
      </v-card-title>
    </slot>

    <v-divider v-if="showTitle"></v-divider>

    <slot></slot>

    <v-container v-if="user"
      class="pt-0"
    >
      <v-row>
        <v-col v-if="!hideUid"
          class="pt-0"
        >
          <display-user-auth
            v-model="user"
            show-uid
            :show-email="false"
            class="py-0"
          ></display-user-auth>
        </v-col>
      </v-row>

      <v-row v-if="!hideAuth"
        class="pt-0"
      >
        <v-col cols="auto" class="pt-0">
          <display-user-auth
            v-model="user"
            show-flags
            show-roles
            class="py-0"
          ></display-user-auth>
        </v-col>

        <v-col v-if="!hideProfile"
          class="pt-0"
        >
          <display-user
            v-model="user"
            :show-email="false"
            class="py-0"
          ></display-user>
        </v-col>
      </v-row>
    </v-container>

    <v-card-actions v-if="!hideActions"
      class="pt-0"
    >
      <slot name="actions">
        <v-spacer></v-spacer>

        <v-btn
          color="secondary"
          @click="$emit('cancel')"
        >
          Close
        </v-btn>
      </slot>
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
  @Prop({ default: 'User Details' }) private title?: string;
  @Prop([Boolean]) private hideTitle?: boolean;
  @Prop([Boolean]) private hideActions?: boolean;
  @Prop([Boolean]) private hideUid?: boolean;
  @Prop([Boolean]) private hideAuth?: boolean;
  @Prop([Boolean]) private hideProfile?: boolean;

  // Computed
  get showTitle() {
    if (this.title) {
      return (this.hideTitle ? false : true);
    }
    return false;
  }

}
</script>

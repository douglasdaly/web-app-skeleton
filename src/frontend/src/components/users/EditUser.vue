<template>
  <v-container fluid>
    <edit-name
      ref="nameForm"
      v-model="nameUpdate"
      @submit="$emit('submit')"
      @cancel="$emit('cancel')"
    ></edit-name>
  </v-container>
</template>

<script lang="ts">
import { Component, Model, Vue } from 'vue-property-decorator';

import api from '@/api';
import { IUser, INameUpdate } from '@/api/schema';
import EditName from '@/components/names/EditName.vue';

@Component({
  components: {
    EditName,
  },
})
export default class EditUser extends Vue {
  @Model('change') private user!: IUser;

  private nameUpdate: INameUpdate = {
    title: this.user.name ? this.user.name.title : '',
    first: this.user.name ? this.user.name.first : '',
    middle: this.user.name ? this.user.name.middle : '',
    last: this.user.name ? this.user.name.last : '',
    suffix: this.user.name ? this.user.name.suffix : '',
  };

  // Methods
  public validate() {
    let ret = true;
    ret = ret && (this.$refs.nameForm as EditName).valid;
    return ret;
  }

  public async submit() {
    return api.user.updateUserMe(this.nameUpdate);
  }

}
</script>

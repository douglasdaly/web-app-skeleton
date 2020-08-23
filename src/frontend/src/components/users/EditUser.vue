<template>
  <v-container fluid>
    <v-form
      ref="form"
      v-model="valid"
    >
      <edit-name
        ref="nameForm"
        v-model="nameUpdate"
        is-child
        @submit="submit()"
        @cancel="$emit('cancel')"
      ></edit-name>
    </v-form>
  </v-container>
</template>

<script lang="ts">
import { Component, Model, Prop, Vue } from 'vue-property-decorator';

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
  @Prop([Boolean]) private isChild?: boolean;

  private valid = false;
  private nameUpdate: INameUpdate = {
    title: this.user.name ? this.user.name.title : '',
    first: this.user.name ? this.user.name.first : '',
    middle: this.user.name ? this.user.name.middle : '',
    last: this.user.name ? this.user.name.last : '',
    suffix: this.user.name ? this.user.name.suffix : '',
    preferred: this.user.name ? this.user.name.preferred : '',
  };

  // Methods
  public validate() {
    let ret = true;
    ret = ret && (this.$refs.nameForm as EditName).valid;
    this.valid = ret;
    return ret;
  }

  public async submit(isChild?: boolean) {
    const child = isChild === false ? false : this.isChild;
    if (child) {
      this.$emit('submit');
    } else {
      if (!!child || this.validate())
      {
        await api.user.updateUserMe(this.nameUpdate);
      }
    }
  }

}
</script>

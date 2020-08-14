<template>
  <v-form
    ref="form"
    v-model="valid"
  >
    <v-container fluid>
      <v-row>
        <v-col>
          <v-text-field
            v-model="name.title"
            label="Title"
          ></v-text-field>
        </v-col>
      </v-row>
      <v-row>
        <v-col>
          <v-text-field
            v-model="name.first"
            :rules="firstRules"
            label="First Name"
            required
          ></v-text-field>
        </v-col>
      </v-row>
      <v-row>
        <v-col>
          <v-text-field
            v-model="name.middle"
            label="Middle Name"
          ></v-text-field>
        </v-col>
      </v-row>
      <v-row>
        <v-col>
          <v-text-field
            v-model="name.last"
            :rules="lastRules"
            label="Last Name"
            required
          ></v-text-field>
        </v-col>
      </v-row>
      <v-row>
        <v-col>
          <v-text-field
            v-model="name.suffix"
            label="Suffix"
          ></v-text-field>
        </v-col>
      </v-row>
    </v-container>
  </v-form>
</template>

<script lang="ts">
import { Component, Model, PropSync, Watch, Vue } from 'vue-property-decorator';

import { IName, INameUpdate } from '@/api/schema';

@Component
export default class EditName extends Vue {
  @Model('change') private name!: INameUpdate;

  public valid = false;

  // Validation
  get firstRules() {
    return [
      (v: string) => !!v || 'First name is required',
    ];
  }

  get lastRules() {
    return [
      (v: string) => !!v || 'Last name is required',
    ];
  }

  public validate() {
    this.valid = (this.$refs.form as HTMLFormElement).validate();
  }
}
</script>

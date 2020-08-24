<template>
  <v-form
    ref="form"
    v-model="valid"
  >
    <v-list>

      <!-- Name Title -->
      <v-list-item>
        <v-list-item-avatar v-if="showIcons">
          <v-icon>mdi-account</v-icon>
        </v-list-item-avatar>

        <v-list-item-content>
          <v-text-field
            v-model="name.title"
            label="Title"
            @keyup.enter="submit()"
            @keyup.esc="$emit('cancel')"
          ></v-text-field>
        </v-list-item-content>
      </v-list-item>

      <!-- First Name -->
      <v-list-item>
        <v-list-item-avatar v-if="showIcons"></v-list-item-avatar>

        <v-list-item-content>
          <v-text-field
            v-model="name.first"
            :rules="firstRules"
            label="First Name"
            required
            @keyup.enter="submit()"
            @keyup.esc="$emit('cancel')"
          ></v-text-field>
        </v-list-item-content>
      </v-list-item>

      <!-- Middle Name -->
      <v-list-item>
        <v-list-item-avatar v-if="showIcons"></v-list-item-avatar>

        <v-list-item-content>
          <v-text-field
            v-model="name.middle"
            label="Middle Name"
            @keyup.enter="submit()"
            @keyup.esc="$emit('cancel')"
          ></v-text-field>
        </v-list-item-content>
      </v-list-item>

      <!-- Last Name -->
      <v-list-item>
        <v-list-item-avatar v-if="showIcons"></v-list-item-avatar>

        <v-list-item-content>
          <v-text-field
            v-model="name.last"
            :rules="lastRules"
            label="Last Name"
            required
            @keyup.enter="submit()"
            @keyup.esc="$emit('cancel')"
          ></v-text-field>
        </v-list-item-content>
      </v-list-item>

      <!-- Suffix -->
      <v-list-item>
        <v-list-item-avatar v-if="showIcons"></v-list-item-avatar>

        <v-list-item-content>
          <v-text-field
            v-model="name.suffix"
            label="Suffix"
            @keyup.enter="submit()"
            @keyup.esc="$emit('cancel')"
          ></v-text-field>
        </v-list-item-content>
      </v-list-item>

      <!-- Preferred Name -->
      <v-list-item>
        <v-list-item-avatar v-if="showIcons"></v-list-item-avatar>

        <v-list-item-content>
          <v-text-field
            v-model="name.preferred"
            label="Preferred Name"
            @keyup.enter="submit()"
            @keyup.esc="$emit('cancel')"
          ></v-text-field>
        </v-list-item-content>
      </v-list-item>
    </v-list>
  </v-form>
</template>

<script lang="ts">
import { Component, Model, Prop, Vue } from 'vue-property-decorator';

import { INameCreate } from '@/api/schema';

function createBlankName(): INameCreate {
  return {
    title: '',
    first: '',
    middle: '',
    last: '',
    suffix: '',
    preferred: '',
  };
};

@Component
export default class CreateName extends Vue {
  @Model('change', { default: () => createBlankName() }) private name!: INameCreate;
  @Prop([String]) private title?: string;
  @Prop([Boolean]) private isChild?: boolean;
  @Prop({ default: true }) showIcons!: boolean;

  public valid = false;

  // Hooks
  mounted() {
    this.name.title = this.name.title || '';
    this.name.first = this.name.first || '';
    this.name.middle = this.name.middle || '';
    this.name.last = this.name.last || '';
    this.name.suffix = this.name.suffix || '';
    this.name.preferred = this.name.preferred || '';
  }

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

  // Functions
  public validate() {
    this.valid = (this.$refs.form as HTMLFormElement).validate();
    return this.valid;
  }

  public reset() {
    (this.$refs.form as HTMLFormElement).reset();
    this.valid = false;
  }

  public submit(isChild?: boolean) {
    const child = isChild === false ? false : this.isChild;
    if (child) {
      this.$emit('submit');
    }
  }
}
</script>

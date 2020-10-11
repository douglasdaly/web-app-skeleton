<template>
  <v-form
    ref="form"
    v-model="valid"
  >
    <v-list>
      <!-- Email address -->
      <v-list-item>
        <v-list-item-avatar v-if="showIcons">
          <v-icon>mdi-mail</v-icon>
        </v-list-item-avatar>

        <v-list-item-content>
          <v-text-field
            ref="emailField"
            v-model="user.email"
            :rules="emailRules"
            label="Email"
            required
            @keydown.esc="$emit('cancel')"
          ></v-text-field>
        </v-list-item-content>
      </v-list-item>

      <!-- Password -->
      <v-list-item>
        <v-list-item-avatar v-if="showIcons">
          <v-icon>mdi-lock</v-icon>
        </v-list-item-avatar>

        <v-list-item-content>
          <v-text-field
            v-model="user.password"
            :rules="passwordRules"
            :type="showPassword ? 'text' : 'password'"
            label="New Password"
            required
            @click:append="showPassword = !showPassword"
            @keydown.esc="$emit('cancel')"
          >
            <template v-slot:append>
              <v-btn
                icon
                tabindex="-1"
                @click="showPassword = !showPassword"
              >
                <v-icon v-if="showPassword">mdi-eye</v-icon>
                <v-icon v-else>mdi-eye-off</v-icon>
              </v-btn>
            </template>
          </v-text-field>
        </v-list-item-content>
      </v-list-item>

      <!-- Confirm Password -->
      <v-list-item>
        <v-list-item-avatar v-if="showIcons"></v-list-item-avatar>

        <v-list-item-content>
          <v-text-field
            v-model="confirmPassword"
            :rules="confirmRules"
            :type="showPassword ? 'text' : 'password'"
            label="Confirm New Password"
            required
            @keyup.enter.stop="submit()"
            @keyup.esc="$emit('cancel')"
          >
            <template v-slot:append>
              <v-btn
                icon
                tabindex="-1"
                @click="showPassword = !showPassword"
              >
                <v-icon v-if="showPassword">mdi-eye</v-icon>
                <v-icon v-else>mdi-eye-off</v-icon>
              </v-btn>
            </template>
          </v-text-field>
        </v-list-item-content>
      </v-list-item>
    </v-list>
  </v-form>
</template>

<script lang="ts">
import { Component, Model, Prop, Vue } from 'vue-property-decorator';

import { IUserCreate } from '@/api/schema';

@Component
export default class CreateUserCredentials extends Vue {
  @Model('change') private user!: IUserCreate;
  @Prop([Boolean]) private isChild?: boolean;
  @Prop({ default: true }) private showIcons!: boolean;

  public valid = false;

  private confirmPassword = '';
  private showPassword = false;

  // Hooks
  mounted() {
    this.focus();
  }

  // Validation
  get emailRules() {
    return [
      (v: string) => !!v || 'E-mail is required',
      (v: string) => /.+@.+\..+/.test(v) || 'E-mail must be valid',
    ];
  }

  get passwordRules() {
    return [
      (v: string) => !!v || 'Password is required',
    ];
  }

  get confirmRules() {
    return [
      (v: string) => v === this.user.password || 'Passwords do not match',
    ];
  }

  // Functions
  public focus() {
    this.$nextTick(() => {
      (this.$refs.emailField as HTMLFormElement).focus();
    });
  }

  public validate() {
    this.valid = (this.$refs.form as HTMLFormElement).validate();
    return this.valid;
  }

  public reset() {
    this.showPassword = false;
    (this.$refs.form as HTMLFormElement).reset();
    this.confirmPassword = '';
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

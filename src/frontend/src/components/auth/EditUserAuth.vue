<template>
  <v-form
    ref="form"
    v-model="valid"
  >
    <v-container fluid>
      <v-row>
        <v-col>
          <v-text-field
            v-model="creds.newEmail"
            :rules="emailRules"
            label="New Email"
            required
            @keydown.enter="submit()"
            @keydown.esc="$emit('cancel')"
          ></v-text-field>
        </v-col>
      </v-row>
      <v-row>
        <v-col>
          <v-text-field
            v-model="creds.newPassword"
            :rules="passwordRules"
            :append-icon="showPassword1 ? 'mdi-eye' : 'mdi-eye-off'"
            :type="showPassword1 ? 'text' : 'password'"
            label="New Password"
            @click:append="showPassword1 = !showPassword1"
            @keydown.esc="$emit('cancel')"
          ></v-text-field>
        </v-col>
      </v-row>
      <v-row>
        <v-col>
          <v-text-field
            v-model="confirmPassword"
            :rules="confirmRules"
            :append-icon="showPassword2 ? 'mdi-eye' : 'mdi-eye-off'"
            :type="showPassword2 ? 'text' : 'password'"
            label="Confirm New Password"
            :required="creds.newPassword ? true : false"
            @click:append="showPassword2 = !showPassword2"
            @keydown.enter="submit()"
            @keydown.esc="$emit('cancel')"
          ></v-text-field>
        </v-col>
      </v-row>
    </v-container>
  </v-form>
</template>

<script lang="ts">
import { Component, Model, Prop, Vue } from 'vue-property-decorator';

export interface UserAuthUpdate {
  newEmail?: string;
  newPassword?: string;
}

@Component
export default class EditUserAuth extends Vue {
  @Model('change') private creds!: UserAuthUpdate;
  @Prop([Boolean]) private isChild?: boolean;

  public valid = false;
  private confirmPassword = '';

  private showPassword1 = false;
  private showPassword2 = false;

  // Validation
  get emailRules() {
    return [
      (v: string) => !!v || 'E-mail is required',
      (v: string) => /.+@.+\..+/.test(v) || 'E-mail must be valid',
    ];
  }

  get passwordRules() {
    return [];
  }

  get confirmRules() {
    return [
      (v: string) => {
        if (this.creds.newPassword) {
          return v === this.creds.newPassword || 'Passwords do not match';
        } else {
          return true;
        }
      },
    ];
  }

  // Functions
  public validate() {
    this.valid = (this.$refs.form as HTMLFormElement).validate();
    return this.valid;
  }

  public submit(isChild?: boolean) {
    const child = isChild === false ? false : this.isChild;
    if (child) {
      this.$emit('submit');
    }
  }

}
</script>

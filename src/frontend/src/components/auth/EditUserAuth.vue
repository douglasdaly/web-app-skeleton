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
          ></v-text-field>
        </v-col>
      </v-row>
      <v-row>
        <v-col>
          <v-text-field
            v-model="creds.newPassword"
            :rules="passwordRules"
            label="New Password"
          ></v-text-field>
        </v-col>
      </v-row>
      <v-row>
        <v-col>
          <v-text-field
            v-model="confirmPassword"
            :rules="confirmRules"
            label="Confirm New Password"
            :required="creds.newPassword ? true : false"
          ></v-text-field>
        </v-col>
      </v-row>
    </v-container>
  </v-form>
</template>

<script lang="ts">
import { Component, Model, Vue } from 'vue-property-decorator';

export interface UserAuthUpdate {
  newEmail?: string;
  newPassword?: string;
}

@Component
export default class EditUserAuth extends Vue {
  @Model('change') private creds!: UserAuthUpdate;

  public valid = false;
  private confirmPassword = '';

  // Validation
  get emailRules() {
    return [];
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

  public validate() {
    this.valid = (this.$refs.form as HTMLFormElement).validate();
  }

}
</script>

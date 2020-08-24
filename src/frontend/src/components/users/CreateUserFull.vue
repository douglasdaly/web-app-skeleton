<template>
  <v-card
    :loading="loading"
  >
    <v-list-item>
      <v-list-item-content>
        <v-list-item-title class="headline">
          Create New User
        </v-list-item-title>
      </v-list-item-content>

      <v-spacer></v-spacer>

      <v-list-item-action>
        <v-btn
          icon
          dark
          color="error"
          @click="cancel()"
        >
          <v-icon>mdi-close</v-icon>
        </v-btn>
      </v-list-item-action>
    </v-list-item>

    <v-divider class="pb-1"></v-divider>

    <!-- Stepper -->
    <v-container fluid
      class="pt-1 pb-0 px-2"
    >
      <v-stepper
        v-model="newUserStep"
      >
        <v-stepper-header>
          <v-stepper-step
            :complete="newUserStep > 1"
            step="1"
          >
            Login Credentials
          </v-stepper-step>

          <v-divider></v-divider>

          <v-stepper-step
            :complete="newUserStep > 2"
            step="2"
          >
            Roles & Permissions
          </v-stepper-step>

          <v-divider></v-divider>

          <v-stepper-step
            :complete="newUserStep > 3"
            step="3"
          >
            User Profile
          </v-stepper-step>

          <v-divider></v-divider>

          <v-stepper-step
            :complete="newUserStep > 4"
            step="4"
          >
            Confirmation
          </v-stepper-step>
        </v-stepper-header>

        <v-stepper-items>
          <!-- Create login credentials -->
          <v-stepper-content step="1">
            <create-user-credentials
              :ref="`formStep1`"
              v-model="user"
              is-child
            ></create-user-credentials>
          </v-stepper-content>

          <!-- Configure user permissions -->
          <v-stepper-content step="2">
            <modify-user-permissions
              ref="formStep2"
              v-model="user"
              is-child
            ></modify-user-permissions>
          </v-stepper-content>

          <!-- Setup user profile information -->
          <v-stepper-content step="3">
            <!-- Name input -->
            <create-name
              ref="formStep3"
              v-model="user.name"
              is-child
            ></create-name>
          </v-stepper-content>

          <!-- Confirm all data -->
          <v-stepper-content step="4">
            <display-user-detailed
              v-model="user"
              title="Confirm User Information"
              class="pa-0 ma-0"
            ></display-user-detailed>
          </v-stepper-content>

        </v-stepper-items>
      </v-stepper>
    </v-container>

    <!-- Card actions -->
    <v-card-actions>
      <v-btn v-if="newUserStep <= 1"
        color="error"
        @click="newUserPrevStep"
      >
        Cancel
      </v-btn>
      <v-btn v-else
        color="secondary"
        :loading="loading"
        @click="newUserPrevStep"
      >
        &lt; Back
      </v-btn>

      <v-spacer></v-spacer>

      <v-btn v-if="newUserStep < 4"
        color="primary"
        @click="newUserNextStep"
      >
        Continue &gt;
      </v-btn>
      <v-btn v-else
        color="success"
        :loading="loading"
        @click="newUserNextStep"
      >
        Create User
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script lang="ts">
import { Component, Model, Vue } from 'vue-property-decorator';

import api from '@/api';
import { IUserCreate } from '@/api/schema';

import CreateName from '@/components/names/CreateName.vue';
import CreateUserCredentials from '@/components/auth/CreateUserCredentials.vue';
import DisplayUserDetailed from './DisplayUserDetailed.vue';
import ModifyUserPermissions from '@/components/auth/ModifyUserPermissions.vue';

function createBlankUser(): IUserCreate {
  return {
    email: '',
    password: '',
    name: {
      first: '',
      last: '',
    },
    roles: [],
    isActive: true,
    isSuperuser: false,
    isAdmin: false,
  };
};

@Component({
  components: {
    CreateName,
    CreateUserCredentials,
    DisplayUserDetailed,
    ModifyUserPermissions,
  }
})
export default class CreateUserFull extends Vue {
  @Model('change', { default: () => createBlankUser() }) private user!: IUserCreate;

  public valid = false;
  private loading = false;
  private newUserStep = 1;

  // Functions
  private async newUserNextStep() {
    let stepValid = false;
    if (this.newUserStep < 4) {
      const formRef = `formStep${this.newUserStep}`;
      stepValid = (this.$refs[formRef] as HTMLFormElement).validate();
    } else {
      stepValid = true;
    }
    if (stepValid) {
      this.newUserStep += 1;
      if (this.newUserStep > 4) {
        await this.submit();
      }
    }
  }

  private newUserPrevStep() {
    if (this.newUserStep > 1) {
      this.newUserStep -= 1;
    } else {
      this.cancel();
    }
  }

  public validate() {
    const ret = ((this.$refs.formStep1 as HTMLFormElement).validate())
      && ((this.$refs.formStep2 as HTMLFormElement).validate())
      && ((this.$refs.formStep3 as HTMLFormElement).validate());
    this.valid = ret;
    return ret;
  }

  public reset() {
    (this.$refs.formStep1 as HTMLFormElement).reset();
    (this.$refs.formStep2 as HTMLFormElement).reset();
    (this.$refs.formStep3 as HTMLFormElement).reset();
    this.newUserStep = 1;
    this.valid = false;
  }

  public async submit() {
    this.loading = true;
    if (this.validate()) {
      await api.user.createUser(this.user);
      this.$emit('submit');
      this.reset();
    }
    this.loading = false;
  }

  public cancel() {
    this.$emit('cancel');
    this.reset();
  }
}
</script>

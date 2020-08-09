<template>
  <v-card
    class="elevation-12"
    :loading="loading"
  >
    <v-toolbar
      dark
      :color="loading ? 'secondary' : 'primary'"
    >
      <v-toolbar-title>{{ title }}</v-toolbar-title>
      <v-spacer></v-spacer>
    </v-toolbar>
    <v-card-text>
      <v-form
        ref="loginForm"
        :disabled="loading"
        @keyup.enter="submit"
      >
        <v-text-field
          v-model="email"
          prepend-icon="mdi-email"
          name="email"
          label="Email"
          ref="emailField"
          type="text"
          @keyup.enter="submit"
        ></v-text-field>
        <v-text-field
          v-model="password"
          prepend-icon="mdi-lock"
          name="password"
          label="Password"
          ref="passwordField"
          :type="passwordType"
          @keyup.enter="submit"
        ></v-text-field>
      </v-form>
      <div v-if="loginError">
        <v-alert
          :value="loginError"
          transition="fade-transition"
          type="error"
        >
          Incorrect email or password.
        </v-alert>
      </div>
      <v-flex class="caption text-xs-right">
        <router-link
          v-if="!loading"
          to="/recover-password"
        >
          Forgot your password?
        </router-link>
        <span
          v-else
          class="text--secondary"
        >
          Forgot your password?
        </span>
      </v-flex>
    </v-card-text>
    <v-card-actions>
      <v-spacer></v-spacer>
      <v-btn
        :color="loading ? 'secondary' : 'primary'"
        @click.prevent="submit"
        :loading="loading"
        :disabled="!valid"
      >
        Login
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script lang="ts">
import { Component, Vue, Watch } from 'vue-property-decorator';
import { Route } from 'vue-router';
import { Dictionary } from 'vue-router/types/router';

import AuthModule from '@/store/modules/auth';

@Component
export default class LoginForm extends Vue {
  private valid = true;
  private loading = false;
  private email = '';
  private password = '';
  private title = 'Login';
  private redirect?: string;
  private otherQuery: Dictionary<string> = {};
  private passwordType = 'password';

  // Computed
  public get loginError(): boolean {
    return AuthModule.loginError;
  }

  // Hooks
  @Watch('$route', { immediate: true })
  private onRouteChange(route: Route) {
    const query = route.query as Dictionary<string>;
    if (query) {
      this.redirect = query.redirect;
      this.otherQuery = this.getOtherQuery(query);
    }
  }

  mounted() {
    if (this.email === '') {
      (this.$refs.emailField as HTMLFormElement).focus();
    } else if (this.password === '') {
      (this.$refs.passwordField as HTMLFormElement).focus();
    }
  }

  // Functions
  private showPassword() {
    if (this.passwordType === 'password') {
      this.passwordType = 'text';
    } else {
      this.passwordType = 'password';
    }
    this.$nextTick(() => {
      (this.$refs.password as HTMLFormElement).focus();
    });
  }

  public async submit() {
    this.loading = true;
    const result = await AuthModule.Login({ email: this.email, password: this.password });
    if (result === true) {
      this.$router.push({
        path: this.redirect || '/',
        query: this.otherQuery,
      });
    }
    this.loading = false;
  }

  private getOtherQuery(query: Dictionary<string>) {
    return Object.keys(query).reduce((acc, cur) => {
      if (cur !== 'redirect') {
        acc[cur] = query[cur];
      }
      return acc;
    }, {} as Dictionary<string>);
  }
}
</script>

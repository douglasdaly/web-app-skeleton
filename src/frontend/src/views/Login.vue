<template>
  <v-container fluid>
    <v-row
      justify="center"
      align="center"
    >
      <v-col xs=12 sm=8 md=4>
        <login-form></login-form>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';

import LoginForm from '@/components/auth/LoginForm.vue';

@Component({
  components: {
    LoginForm,
  },
})
export default class Login extends Vue {
}
</script>

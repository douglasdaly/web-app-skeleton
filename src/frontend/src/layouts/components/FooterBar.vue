<template>
  <!-- Footer -->
  <v-footer
    app
    color="secondary"
    dark
  >
    <span>Made with <span class="red--text">❤️</span> by
      <a href="https://github.com/douglasdaly/"
        target="_blank"
        v-text="'Doug'"
      ></a>
    </span>
    <v-spacer></v-spacer>
    <span>&copy; {{ new Date().getFullYear() }}</span>
  </v-footer>
</template>

<script>
import { Component, Vue } from 'vue-property-decorator';

@Component
export default class FooterBar extends Vue {
}
</script>

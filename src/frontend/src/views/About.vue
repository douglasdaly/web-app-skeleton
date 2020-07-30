<template>
  <v-container px-8>
    <v-row>
      <v-col>
        <h1>About</h1>
        <p>
          This is basic skeleton for a modern web application.  It's written in
          <a href="https://www.python.org/" target="_blank">Python</a> for the
          back-end API and
          <a href="https://www.typescriptlang.org/" target="_blank">TypeScript</a>
          for the front-end web-based UI.
        </p>
        <p>
          The backend is powered by (the <i>exceptional</i>)
          <a href="https://fastapi.tiangolo.com/" target="_blank">FastAPI</a>
          Python package for high-performance, asyncronous, and
          developer-friendly APIs.  FastAPI allows developers to (quickly)
          write APIs without worrying about the details of validation,
          transport, routing, etc.
        </p>
        <p>
          The frontend is powered by (the <i>amazing</i>)
          <a href="https://vuejs.org/" target="_blank">Vue.js</a> framework
          for progressive web applications.  A number of additional Vue
          libraries are utilized to make everything work together and to allow
          for rapid development of additional components.
        </p>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';

@Component
export default class About extends Vue {
}
</script>

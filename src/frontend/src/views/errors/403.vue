<template>
  <v-container fluid>
    <error-card
      :code="403"
      title="Forbidden"
    ></error-card>
  </v-container>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';

import ErrorCard from '@/components/utilities/ErrorCard.vue';

@Component({
  components: {
    ErrorCard,
  }
})
export default class Error403 extends Vue {
};
</script>

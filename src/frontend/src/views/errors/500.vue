<template>
  <v-container fluid>
    <error-card
      :code="500"
      title="Internal Server Error"
      detail="An error occurred on the server."
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
export default class Error500 extends Vue {
};
</script>

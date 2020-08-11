<template>
  <v-container fluid>
    <error-card
      :code="400"
      title="Bad Request"
      detail="An error occurred."
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
export default class Error400 extends Vue {
};
</script>

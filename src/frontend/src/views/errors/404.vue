<template>
  <v-container fluid>
    <error-card
      :code="404"
      title="Not Found"
      detail="The resource you requested could not be found."
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
export default class Error404 extends Vue {
};
</script>

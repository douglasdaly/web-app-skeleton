<template>
  <v-container fluid>
    <error-card
      :code="401"
      title="Unauthorized"
      detail="You do not have sufficient privileges."
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
export default class Error401 extends Vue {
};
</script>

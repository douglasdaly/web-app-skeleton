<template>
  <v-card
    dark
    class="mx-auto"
    max-width="344"
    outlined
  >
    <v-list-item three-line>
      <v-list-item-content>
        <div v-if="displayStatus"
          class="overline mb-4"
        >
          {{ displayStatus }}
        </div>

        <v-list-item-title v-if="displayTitle"
          class="headline mb-1"
        >
          {{ displayTitle }}
        </v-list-item-title>

        <v-list-item-subtitle v-if="detail">
          {{ detail }}
        </v-list-item-subtitle>

        <slot></slot>
      </v-list-item-content>

      <v-list-item-avatar
        icon
        color="error"
      >
        <v-icon large>mdi-alert-circle-outline</v-icon>
      </v-list-item-avatar>
    </v-list-item>

    <v-card-actions>
      <v-btn
        color="secondary"
        @click="goBack"
      >
        <v-icon small class="pr-1">mdi-arrow-left-circle</v-icon>
        Back
      </v-btn>

      <v-spacer></v-spacer>

      <v-btn to="/"
        color="primary"
      >
        <v-icon small class="pr-1">mdi-home</v-icon>
        Home
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';

@Component
export default class ErrorCard extends Vue {
  @Prop([String]) private status?: string;
  @Prop([Number]) private code?: number;
  @Prop([String]) private title?: string;
  @Prop([String]) private detail?: string;

  // Computed
  get displayStatus(): string {
    if (this.status) {
      return this.status.toUpperCase();
    }
    else if (this.code) {
      return `${this.code} ERROR`;
    }
    return '';
  }

  get displayTitle(): string | undefined {
    if (this.title) {
      return this.title;
    } else if (!this.displayStatus) {
      return 'Error';
    }
  }

  // Functions
  private goBack() {
    this.$router.go(-1);
  }
};
</script>

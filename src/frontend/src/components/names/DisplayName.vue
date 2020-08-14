<template>
  <v-list two-line>
    <v-list-item v-if="name && name.title">
      <v-list-item-avatar v-if="showIcons">
        <v-icon>
          mdi-account
        </v-icon>
      </v-list-item-avatar>

      <v-list-item-content>
        <v-list-item-title>{{ name.title }}</v-list-item-title>
        <v-list-item-subtitle>Title</v-list-item-subtitle>
      </v-list-item-content>
    </v-list-item>

    <v-list-item>
      <v-list-item-avatar v-if="showIcons">
        <v-icon v-if="!name || !name.title">
          mdi-account
        </v-icon>
      </v-list-item-avatar>

      <v-list-item-content>
        <v-list-item-title v-if="name">
          {{ name.first }}
        </v-list-item-title>
        <v-list-item-title v-else
          class="grey--text"
        >
          &lt;Not Set&gt;
        </v-list-item-title>
        <v-list-item-subtitle>First Name</v-list-item-subtitle>
      </v-list-item-content>
    </v-list-item>

    <v-list-item v-if="name && name.middle">
      <v-list-item-avatar v-if="showIcons"></v-list-item-avatar>

      <v-list-item-content>
        <v-list-item-title>{{ name.middle }}</v-list-item-title>
        <v-list-item-subtitle>Middle Name</v-list-item-subtitle>
      </v-list-item-content>
    </v-list-item>

    <v-list-item>
      <v-list-item-avatar v-if="showIcons"></v-list-item-avatar>

      <v-list-item-content>
        <v-list-item-title v-if="name">
          {{ name.last }}
        </v-list-item-title>
        <v-list-item-title v-else
          class="grey--text"
        >
          &lt;Not Set&gt;
        </v-list-item-title>
        <v-list-item-subtitle>Last Name</v-list-item-subtitle>
      </v-list-item-content>
    </v-list-item>

    <v-list-item v-if="name && name.suffix">
      <v-list-item-avatar v-if="showIcons"></v-list-item-avatar>

      <v-list-item-title>
        {{ name.suffix }}
      </v-list-item-title>
      <v-list-item-subtitle>Suffix</v-list-item-subtitle>
    </v-list-item>
  </v-list>
</template>

<script lang="ts">
import { Component, Model, Prop, Vue } from 'vue-property-decorator';

import { IName } from '@/api/schema';

@Component
export default class DisplayName extends Vue {
  @Model('change') private name?: IName;
  @Prop({ default: true }) private readonly showIcons!: boolean;
}
</script>

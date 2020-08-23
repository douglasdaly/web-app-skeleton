<template>
  <v-card dark color="secondary">
    <v-list-item>
      <v-list-item-content>
        <v-list-item-title v-if="title"
          class="headline-2"
        >
          {{ title }}
        </v-list-item-title>
      </v-list-item-content>
    </v-list-item>

    <v-divider v-if="title"></v-divider>

    <v-list dense light>
      <v-list-item v-for="(route, key) in routes"
        :key="`${route.name}-${key}`"
        :to="route.path"
      >
        <v-list-item-icon>
          <v-icon v-if="route.meta && route.meta.icon">
            {{ route.meta.icon }}
          </v-icon>
        </v-list-item-icon>

        <v-list-item-content>
          <v-list-item-title v-if="route.meta && route.meta.title">
            {{ route.meta.title }}
          </v-list-item-title>
        </v-list-item-content>
      </v-list-item>
    </v-list>
  </v-card>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';
import { RouteConfig } from 'vue-router';

@Component
export default class Sidebar extends Vue {
  @Prop() readonly title?: string;
  @Prop({ required: true }) readonly routes!: RouteConfig[];
};
</script>

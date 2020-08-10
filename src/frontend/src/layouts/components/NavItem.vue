<template>
  <v-list-group v-if="visibleChildren.length > 1"
    :prepend-icon="(item.meta && item.meta.icon) ? item.meta.icon : undefined"
  >
    <template v-if="item.meta && item.meta.title"
      v-slot:activator
    >
      <v-list-item-title>{{ item.meta.title }}</v-list-item-title>
    </template>

    <span>{{ item.path }}</span>
    <ul v-if="visibleChildren">
      <li v-for="(child, index) in visibleChildren"
        :key="`${child.path}-${index}`"
      >
        {{ child.path }}
      </li>
    </ul>
  </v-list-group>
  <v-list-item v-else-if="onlyChild"
    :to="`${item.path}${onlyChild.path}`"
  >
    <v-list-item-action v-if="onlyChild.meta && onlyChild.meta.icon">
      <v-icon>{{ onlyChild.meta.icon }}</v-icon>
    </v-list-item-action>
    <v-list-item-content v-if="onlyChild.meta && onlyChild.meta.title">
      {{ onlyChild.meta.title }}
    </v-list-item-content>
  </v-list-item>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';
import { RouteConfig } from 'vue-router';

@Component
export default class NavItem extends Vue {
  @Prop({ required: true }) private item!: RouteConfig;

  // Getters
  get visibleChildren(): RouteConfig[] {
    if (!this.item.children || (this.item.meta && this.item.meta.hidden)) {
      return [];
    }
    const result = this.item.children.filter((item) => {
      if (item.meta && item.meta.hidden) {
        return false;
      } else {
        return true;
      }
    });
    return result;
  }

  get onlyChild(): RouteConfig | null {
    if (this.visibleChildren.length == 1) {
      return this.visibleChildren[0];
    }
    return null;
  }
}

</script>

<template>
  <div>
    <v-menu v-if="canCollapse && collapsed"
      :open-on-hover="openOnHover"
      :dark="dark"
      bottom
      offset-y
    >
      <template v-slot:activator="{ on, attrs }">
        <v-btn
          v-bind="attrs"
          v-on="on"
          icon
          small
        >
          <v-icon
            small
            color="secondary"
          >
            mdi-dots-vertical-circle
          </v-icon>
        </v-btn>
      </template>

      <v-list dense>
        <v-list-item
          :disabled="disabled || !canView"
          @click="$emit('item-view')"
        >
          <v-list-item-icon class="mx-0">
            <v-icon small>mdi-dots-horizontal-circle</v-icon>
          </v-list-item-icon>
          <v-list-item-title class="mx-0">View</v-list-item-title>
        </v-list-item>

        <v-list-item
          :disabled="disabled || !canEdit"
          @click="$emit('item-edit')"
        >
          <v-list-item-icon class="mx-0">
            <v-icon small>mdi-pencil</v-icon>
          </v-list-item-icon>
          <v-list-item-title class="mx-0">Edit</v-list-item-title>
        </v-list-item>

        <v-list-item
          :disabled="disabled || !canDelete"
          @click="$emit('item-delete')"
        >
          <v-list-item-icon class="mx-0">
            <v-icon small>mdi-delete</v-icon>
          </v-list-item-icon>
          <v-list-item-title class="mx-0">Delete</v-list-item-title>
        </v-list-item>
      </v-list>
    </v-menu>

    <!-- Otherwise show individual action buttons -->
    <div v-else>

      <v-tooltip bottom>
        <template v-slot:activator="{ on, attrs }" left>
          <v-btn
            v-bind="attrs"
            v-on="on"
            :disabled="disabled || !canView"
            icon
            small
            @click="$emit('item-view')"
          >
            <v-icon small>mdi-dots-horizontal-circle</v-icon>
          </v-btn>
        </template>
        <span>View</span>
      </v-tooltip>

      <v-tooltip bottom>
        <template v-slot:activator="{ on, attrs }" left>
          <v-btn
            v-bind="attrs"
            v-on="on"
            :disabled="disabled || !canEdit"
            icon
            small
            @click="$emit('item-edit')"
          >
            <v-icon small>mdi-pencil</v-icon>
          </v-btn>
        </template>
        <span>Edit</span>
      </v-tooltip>

      <v-tooltip bottom>
        <template v-slot:activator="{ on, attrs }" left>
          <v-btn
            v-bind="attrs"
            v-on="on"
            :disabled="disabled || !canDelete"
            icon
            small
            @click="$emit('item-delete')"
          >
            <v-icon small>mdi-delete</v-icon>
          </v-btn>
        </template>
        <span>Delete</span>
      </v-tooltip>
    </div>
  </div>
</template>


<script lang="ts">
import { Component, Model, Prop, Vue } from 'vue-property-decorator';

@Component
export default class ListItemActions extends Vue {
  @Model('change', { default: null }) private collapseState!: boolean | null;
  @Prop({ default: true }) private canCollapse!: boolean;
  @Prop({ default: 'smAndDown' }) private breakpoint!: string;
  @Prop([Boolean]) private disabled?: boolean;

  @Prop([Boolean]) private canView?: boolean;
  @Prop([Boolean]) private canEdit?: boolean;
  @Prop([Boolean]) private canDelete?: boolean;

  @Prop([Boolean]) private dark?: boolean;
  @Prop([Boolean]) private openOnHover?: boolean;

  // Computed
  get collapsed(): boolean {
    if (this.collapseState === null)
    {
      // @ts-ignore: Not recognizing $vuetify object on Vue instances
      return this.$vuetify.breakpoint[this.breakpoint];
    } else {
      return this.collapseState;
    }
  }

}
</script>

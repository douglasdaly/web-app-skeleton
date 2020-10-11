<template>
  <v-list
    flat
    :subheader="title ? true : false"
    :dense="dense"
  >
    <v-subheader v-if="title">{{ title }}</v-subheader>

    <template v-for="(item, idx) in displayItems">
      <v-list-item v-if="!item.hidden"
        :key="`${item.value}-${idx}`"
        :dense="dense"
        @change="$emit('change', selectedValues)"
      >
        <template v-slot:default="{ active }">
          <v-list-item-action
            :class="{ 'mx-0': dense }"
          >
            <v-checkbox
              v-model="item.selected"
              :input-value="active"
              color="primary"
              :disabled="item.disabled"
              :dense="dense"
            ></v-checkbox>
          </v-list-item-action>
          <v-list-item-content
            :class="{ 'mx-1': dense }"
          >
            <v-list-item-subtitle>
              {{ item.text }}
            </v-list-item-subtitle>
          </v-list-item-content>
        </template>
      </v-list-item>
    </template>
  </v-list>
</template>

<script lang="ts">
import { Component, Model, Prop, Vue } from 'vue-property-decorator';

export interface CheckItem {
  value: string;
  text?: string;
  selected?: boolean;
  fixed?: boolean;
  hidden?: boolean;
};

interface DisplayItem {
  value: string;
  text: string;
  selected: boolean;
  disabled: boolean;
  hidden: boolean;
};

@Component
export default class MultiCheckList extends Vue {
  @Model('change') private selected!: string[];
  @Prop() private items!: CheckItem[];
  @Prop({ required: false }) private title?: string;
  @Prop([Boolean]) private dense?: boolean;

  private displayItems: DisplayItem[] = [];

  // Hooks
  mounted() {
    this.items.forEach((x: CheckItem) => {
      const newItem: DisplayItem = {
        value: x.value,
        text: x.text || x.value,
        selected: x.selected === true,
        disabled: x.fixed === true,
        hidden: x.hidden === true,
      };
      this.displayItems.push(newItem);
    });
  }

  // Computed
  get selectableCount(): number {
    return this.items.length - this.selected.length;
  }

  get selectedValues(): string[] {
    const ret: string[] = [];
    this.displayItems.forEach((x: DisplayItem) => {
      if (x.selected) {
        ret.push(x.value);
      }
    });
    return ret;
  }

}
</script>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';

import SidebarLayout from './bases/SidebarLayout.vue';

@Component({
  name: 'AdminLayout',
})
export default class AdminLayout extends SidebarLayout {
  protected title="Administration";
  protected parentPath="/admin";
}
</script>

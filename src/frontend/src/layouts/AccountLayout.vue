<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';

import SidebarLayout from './bases/SidebarLayout.vue';

@Component({
  name: 'AccountLayout',
})
export default class AccountLayout extends SidebarLayout {
  protected title="My Account";
  protected parentPath="/account";
}
</script>

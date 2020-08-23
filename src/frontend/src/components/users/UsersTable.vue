<template>
  <div class="pt-2">
    <v-data-table
      :loading="loading"
      :headers="headers"
      :items="items"
      sort-by="email"
      :show-select="showSelect"
      :single-select="singleSelect"
      :dense="dense"
      :search="search"
      class="elevation-1"
    >
      <template v-slot:top>
        <v-toolbar
          flat
        >
          <!-- Column selection dropdown -->
          <v-menu
            dark
            dense
            bottom
            offset-y
          >
            <template v-slot:activator="{ on: menu, attrs }">
              <v-tooltip top>
                <template v-slot:activator="{ on: tooltip }">
                  <v-btn
                    v-bind="attrs"
                    v-on="{ ...tooltip, ...menu }"
                    icon
                  >
                    <v-icon>mdi-format-list-checkbox</v-icon>
                  </v-btn>
                </template>
                <span>Select Visible Columns</span>
              </v-tooltip>
            </template>
            <multi-check-list
              v-model="selectedColumns"
              :items="selectableHeaders"
              title="Visible Columns"
              dense
            ></multi-check-list>
          </v-menu>

          <!-- Search -->
          <v-text-field
            v-model="search"
            hide-details
            label="Search"
            append-icon="mdi-magnify"
            single-line
          ></v-text-field>

          <v-spacer></v-spacer>

          <!-- New User Button -->
          <v-btn
            color="primary"
            dark
            :disabled="detailsDialog || editDialog || deleteDialog"
            @click="newDialog = true"
          >
            <span class="ml-1">New User</span>
          </v-btn>
        </v-toolbar>
      </template>

      <template v-slot:item.firstName="{ item }">
        <i v-if="!item.firstName"
          color="gray"
        >
          &lt;Not Set&gt;
        </i>
        <span v-else>
          {{ item.firstName }}
        </span>
      </template>

      <template v-slot:item.lastName="{ item }">
        <i v-if="!item.lastName"
          color="gray"
        >
          &lt;Not Set&gt;
        </i>
        <span v-else>
          {{ item.lastName }}
        </span>
      </template>

      <template v-slot:item.isActive="{ item }">
        <v-icon v-if="item.isActive"
          small
        >
          mdi-check
        </v-icon>
        <v-icon v-else
          small
          color="error"
        >
          mdi-close
        </v-icon>
      </template>

      <template v-slot:item.isSuperuser="{ item }">
        <v-icon v-if="item.isSuperuser"
          small
          color="success"
        >
          mdi-check
        </v-icon>
        <v-icon v-else
          small
        >
          mdi-close
        </v-icon>
      </template>

      <template v-slot:item.isAdmin="{ item }">
        <v-icon v-if="item.isAdmin"
          small
          color="success"
        >
          mdi-check
        </v-icon>
        <v-icon v-else
          small
        >
          mdi-close
        </v-icon>
      </template>

      <template v-slot:item.roles="{ item }">
        <span v-if="item.roles">
          {{ item.roles }}
        </span>
        <i v-else color="gray">&lt;None&gt;</i>
      </template>

      <!-- Actions -->
      <template v-slot:item.actions="{ item }">
        <list-item-actions
          v-model="showActions"
          can-view
          can-edit
          can-delete
          open-on-hover
          dark
          @item-view="showUser(item.uid)"
          @item-edit="editUser(item.uid)"
          @item-delete="deleteUser(item.uid)"
        ></list-item-actions>
      </template>

    </v-data-table>

    <!-- New User Dialog -->
    <v-dialog
      v-model="newDialog"
      max-width="650px"
      dark
    >
      <create-user-full
        @cancel="newDialog = false"
        @submit="update()"
      ></create-user-full>
    </v-dialog>

    <!-- Details Dialog -->
    <v-dialog v-model="detailsDialog"
      max-width="650px"
    >
      <display-user-detailed v-if="selectedUser"
        v-model="selectedUser"
        dark
        show-actions
        @cancel="detailsDialog = false"
      ></display-user-detailed>
    </v-dialog>

    <!-- Edit Dialog -->

    <!-- Delete Dialog -->

  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'vue-property-decorator';

import api from '@/api';
import { IUser } from '@/api/schema';

import CreateUserFull from './CreateUserFull.vue';
import DisplayUser from './DisplayUser.vue';
import DisplayUserAuth from '@/components/auth/DisplayUserAuth.vue';
import DisplayUserDetailed from './DisplayUserDetailed.vue';
import ListItemActions from '@/components/utilities/ListItemActions.vue';
import MultiCheckList, { CheckItem } from '@/components/utilities/MultiCheckList.vue';

export interface UserListItem {
  uid: string;
  email: string;
  firstName: string | null;
  lastName: string | null;
  isActive: boolean;
  isSuperuser: boolean;
  isAdmin: boolean;
  roles?: string;
};

export interface ListHeader {
  text: string;
  value: string;
  align?: string;
  sortable?: boolean;
};

@Component({
  components: {
    CreateUserFull,
    DisplayUser,
    DisplayUserAuth,
    DisplayUserDetailed,
    ListItemActions,
    MultiCheckList,
  }
})
export default class UsersTable extends Vue {
  @Prop({ required: false }) private showColumns?: string[];
  @Prop({ default: () => [ 'isAdmin', 'isSuperuser' ] }) private unselectedColumns!: string[];
  @Prop({ default: () => [ 'email', 'actions' ] }) private fixedColumns!: string[];

  @Prop([Boolean]) private dense?: boolean;
  @Prop([Boolean]) private showSelect?: boolean;
  @Prop([Boolean]) private singleSelect?: boolean;

  private loading = true;

  private search = '';
  private selectedColumns: string[] = [];

  private dialogLoading = true;
  private newDialog = false;

  private detailsDialog = false;
  private editDialog = false;
  private deleteDialog = false;

  private selectedUser: IUser | null = null;
  private users: IUser[] = [];
  private page = 0;
  private limit = 20;

  private allHeaders: ListHeader[] = [
    {
      text: 'Email',
      value: 'email',
    },
    {
      text: 'Active?',
      value: 'isActive',
      align: 'center',
    },
    {
      text: 'Last Name',
      value: 'lastName',
    },
    {
      text: 'First Name',
      value: 'firstName',
    },
    {
      text: 'Superuser?',
      value: 'isSuperuser',
      align: 'center',
    },
    {
      text: 'Admin?',
      value: 'isAdmin',
      align: 'center',
    },
    {
      text: 'Role(s)',
      value: 'roles',
    },
    {
      text: 'Actions',
      value: 'actions',
      align: 'center',
      sortable: false,
    }
  ];

  // Hooks
  async mounted() {
    this.availableHeaders.forEach((x: ListHeader) => {
      if (!this.unselectedColumns.includes(x.value)) {
        this.selectedColumns.push(x.value);
      }
    });
    await this.update();
  }

  // Computed
  get showActions(): boolean | null {
    return this.selectedColumns.length > 4 ? null : true;
  }

  get items() {
    const ret: UserListItem[] = [];
    this.users.forEach((user: IUser) => {
      const roleStr = user.roles ? user.roles.map(x => x.name).join(', ') : undefined;
      ret.push({
        uid: user.uid,
        email: user.email,
        lastName: user.name ? user.name.last : null,
        firstName: user.name ? user.name.first : null,
        isActive: user.isActive,
        isSuperuser: user.isSuperuser,
        isAdmin: user.isAdmin,
        roles: roleStr,
      });
    });
    return ret;
  }

  get headers() {
    const ret: ListHeader[] = [];
    this.availableHeaders.forEach((x: ListHeader) => {
      if (this.selectedColumns.includes(x.value)) {
        ret.push(x);
      }
    });
    return ret;
  }

  get availableHeaders() {
    if (this.showColumns) {
      const ret: ListHeader[] = [];
      this.allHeaders.forEach((x: ListHeader) => {
        if (this.showColumns && this.showColumns.includes(x.value)) {
          ret.push(x);
        }
      });
      return ret;
    }
    return this.allHeaders;
  }

  get selectableHeaders() {
    const ret: CheckItem[] = []
    this.availableHeaders.forEach((x: ListHeader) => {
      ret.push({
        value: x.value,
        text: x.text || x.value,
        selected: this.selectedColumns.includes(x.value),
        hidden: this.fixedColumns.includes(x.value),
      });
    });
    return ret;
  }

  // Functions
  // - Get data from database
  public async update() {
    this.loading = true;
    this.newDialog = false;
    this.editDialog = false;
    this.detailsDialog = false;
    this.deleteDialog = false;
    this.users = [];
    const skip = this.page * this.limit;
    await api.user.readUsers(skip, this.limit)
      .then(res => res.forEach((user) => this.users.push(user)));
    this.loading = false;
  }

  // - Table action functions
  public async showUser(userId: string) {
    this.dialogLoading = true;
    this.detailsDialog = true;
    this.selectedUser = await api.user.readUserById(userId);
    this.dialogLoading = false;
  }

  public editUser(userId: string) {
    console.log(userId);
  }

  public deleteUser(userId: string) {
    console.log(userId);
  }
}
</script>

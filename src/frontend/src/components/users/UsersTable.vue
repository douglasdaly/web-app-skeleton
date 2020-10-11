<template>
  <div class="pt-2">
    <v-data-table
      :loading="loading"
      :headers="headers"
      :items="items"
      :page.sync="page"
      :items-per-page.sync="limit"
      :server-items-length="totalUserCount"
      sort-by="email"
      :show-select="showSelect"
      :single-select="singleSelect"
      :dense="dense"
      :search="search"
      class="elevation-1"
      :footer-props="{
        itemsPerPageOptions: [10, 25, 100, -1],
      }"
      @update:items-per-page="update()"
      @update:page="update()"
    >
      <template v-slot:top>
        <v-toolbar
          flat
        >
          <!-- New User Button -->
          <v-tooltip top>
            <template v-slot:activator="{ on, attrs }" left>
              <v-btn
                v-bind="attrs"
                v-on="on"
                fab
                x-small
                dark
                color="primary"
                :disabled="detailsDialog || editDialog || deleteDialog"
                @click="newDialog = true"
              >
                <v-icon>mdi-plus</v-icon>
              </v-btn>
            </template>
            <span>Add New User</span>
          </v-tooltip>

          <!-- Column selection dropdown -->
          <v-menu
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
                    class="ml-2"
                    icon
                    small
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

          <v-spacer></v-spacer>

          <!-- Search -->
          <v-text-field
            v-model="search"
            class="ml-2"
            hide-details
            label="Search"
            prepend-icon="mdi-magnify"
            single-line
          ></v-text-field>

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
          :can-delete="canDelete(item.uid)"
          open-on-hover
          @item-view="showUser(item.uid)"
          @item-edit="startEditUser(item.uid)"
          @item-delete="startDeleteUser(item.uid)"
        ></list-item-actions>
      </template>

    </v-data-table>

    <!-- New User Dialog -->
    <v-dialog
      v-model="newDialog"
      persistent
      max-width="650px"
    >
      <create-user-full
        ref="newUserForm"
        @cancel="cancelCreateUser()"
        @submit="createUser()"
      ></create-user-full>
    </v-dialog>

    <!-- Details Dialog -->
    <v-dialog v-model="detailsDialog"
      max-width="650px"
    >
      <display-user-detailed v-if="selectedUser"
        v-model="selectedUser"
        show-actions
        @cancel="detailsDialog = false"
      ></display-user-detailed>
    </v-dialog>

    <!-- Edit Dialog -->
    <v-dialog v-model="editDialog"
      persistent
      max-width="650px"
    >
      <v-card>
        <edit-user-full
          ref="editUserForm"
          v-model="selectedUser"
          edit-login
          edit-auths
          @cancel="cancelEditUser()"
          @submit="editUser()"
        >
        </edit-user-full>
      </v-card>
    </v-dialog>

    <!-- Delete Dialog -->
    <v-dialog v-model="deleteDialog"
      max-width="450px"
    >
      <display-user-detailed
        ref="deleteUserForm"
        v-model="selectedUser"
        hide-profile
        dark
      >
        <template v-slot:title>
          <v-card-title>
            <v-icon
              large
              color="warning"
            >
              mdi-alert
            </v-icon>
            <span class="headline ml-2">Confirm Delete</span>
          </v-card-title>
        </template>

        <template v-slot:default>
          <v-card-text class="subtitle-1 pt-2 pb-0">
            Are you sure you want to delete this user?
          </v-card-text>
        </template>

        <template v-slot:actions>
          <v-spacer></v-spacer>

          <v-btn
            dark
            color="error"
            @click="deleteUser(selectedUser.uid)"
          >
            <v-icon>mdi-delete</v-icon> Delete
          </v-btn>

          <v-btn
            dark
            color="secondary"
            @click="cancelDeleteUser()"
          >
            Cancel
          </v-btn>
        </template>
      </display-user-detailed>
    </v-dialog>

  </div>
</template>

<script lang="ts">
import { Component, Vue, Prop } from 'vue-property-decorator';

import api from '@/api';
import { IUser } from '@/api/schema';
import AuthModule from '@/store/modules/auth';

import { delayCall } from '@/utils/delayed';

import CreateUserFull from './CreateUserFull.vue';
import DisplayUser from './DisplayUser.vue';
import DisplayUserAuth from '@/components/auth/DisplayUserAuth.vue';
import DisplayUserDetailed from './DisplayUserDetailed.vue';
import EditUserFull from './EditUserFull.vue';
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
    EditUserFull,
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

  private loading = false;
  private totalUserCount = -1;

  private search = '';
  private selectedColumns: string[] = [];

  private dialogLoading = true;
  private newDialog = false;

  private detailsDialog = false;
  private editDialog = false;
  private deleteDialog = false;

  private selectedUser: IUser | null = null;
  private users: IUser[] = [];
  private page = 1;
  private limit = 25;

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
  get currentUser(): IUser | null {
    return AuthModule.user;
  }

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
  // - Check if can delete
  private canDelete(userId: string): boolean {
    if (this.currentUser) {
      return this.currentUser.uid !== userId;
    }
    return false;
  }

  // - Get data from database
  public async update() {
    const loadWait = delayCall(500, () => { this.loading = true; });
    this.newDialog = false;
    this.editDialog = false;
    this.detailsDialog = false;
    this.deleteDialog = false;
    this.users = [];
    this.totalUserCount = await api.user.readUserCount();
    const skip = (this.page - 1) * this.limit;
    await api.user.readUsers(skip, this.limit > 0 ? this.limit : undefined)
      .then(res => res.forEach((user) => this.users.push(user)));
    loadWait.cancel();
    this.loading = false;
  }

  // - Table action functions
  // -- New
  public startCreateUser() {
    this.newDialog = true;
  }

  public async createUser() {
    this.newDialog = false;
    await this.update();
  }

  public cancelCreateUser() {
    this.newDialog = false;
  }

  // -- Display
  public async showUser(userId: string) {
    this.dialogLoading = true;
    this.detailsDialog = true;
    this.selectedUser = await api.user.readUserById(userId);
    this.dialogLoading = false;
  }

  // -- Edit
  public async startEditUser(userId: string) {
    this.dialogLoading = true;
    this.selectedUser = await api.user.readUserById(userId);
    this.editDialog = true;
    this.dialogLoading = false;
  }

  public async editUser() {
    this.editDialog = false;
    this.selectedUser = null;
    await this.update();
  }

  public cancelEditUser() {
    this.editDialog = false;
  }

  // -- Delete
  public async startDeleteUser(userId: string) {
    this.dialogLoading = true;
    this.deleteDialog = true;
    this.selectedUser = await api.user.readUserById(userId);
    this.dialogLoading = false;
  }

  public async deleteUser(userId: string) {
    this.loading = true;
    this.dialogLoading = true;
    await api.user.deleteUser(userId);
    this.dialogLoading = false;
    this.deleteDialog = false;
    this.selectedUser = null;
    await this.update();
    this.loading = false;
  }

  public cancelDeleteUser() {
    this.deleteDialog = false;
    this.selectedUser = null;
  }
}
</script>

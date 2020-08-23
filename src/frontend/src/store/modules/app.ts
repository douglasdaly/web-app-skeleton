import {
  getModule,
  Module,
  Mutation,
  VuexModule,
  Action,
} from 'vuex-module-decorators';

import { appName } from '@/env';
import store from '@/store';
import cookies from '@/utils/cookies';

export enum DeviceType {
  Mobile,
  Desktop,
};

@Module({ name: 'app', dynamic: true, store })
class AppModule extends VuexModule {
  public appTitle: string = appName;
  public drawer = {
    opened: cookies.getDrawerStatus() === 'opened',
  };
  public device = DeviceType.Desktop;

  public cookieNotify = cookies.getCookiesNotified() ? false : true;

  // Mutations
  @Mutation
  private SET_APP_TITLE(title?: string) {
    this.appTitle = title || appName;
  }

  @Mutation
  private SET_DRAWER(opened: boolean) {
    this.drawer.opened = opened;
    if (opened) {
      cookies.setDrawerStatus('opened');
    } else {
      cookies.setDrawerStatus('closed');
    }
  }

  @Mutation
  private SET_DEVICE(device: DeviceType) {
    this.device = device;
  }

  @Mutation
  private SET_COOKIE_NOTIFY(notify: boolean) {
    this.cookieNotify = notify;
    cookies.setCookiesNotified(!notify);
  }

  // Actions
  @Action
  public SetAppTitle(title?: string) {
    this.SET_APP_TITLE(title);
  }

  @Action
  public ToggleDrawer(opened?: boolean) {
    const isOpen = (opened === undefined) ? this.drawer.opened : !opened;
    this.SET_DRAWER(!isOpen);
  }

  @Action
  public OpenDrawer() {
    this.SET_DRAWER(true);
  }

  @Action
  public CloseDrawer() {
    this.SET_DRAWER(false);
  }

  @Action
  public ToggleDevice(device?: DeviceType) {
    if (device) {
      this.SET_DEVICE(device)
    } else {
      if (this.device === DeviceType.Desktop) {
        this.SET_DEVICE(DeviceType.Mobile);
      } else {
        this.SET_DEVICE(DeviceType.Desktop);
      }
    }
  }

  @Action
  public CookiesNotified() {
    this.SET_COOKIE_NOTIFY(false);
  }

}

export default getModule(AppModule);

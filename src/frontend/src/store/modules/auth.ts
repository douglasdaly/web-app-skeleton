import {
  getModule,
  Module,
  Mutation,
  VuexModule,
  Action,
} from 'vuex-module-decorators';

import api from '@/api';
import { IMsg, IUser } from '@/api/schema';
import { resetRouter } from '@/router';
import store from '@/store';
import { getLocalToken, saveLocalToken, removeLocalToken } from '@/utils/jwt';
import { getToken, removeToken, setToken } from '@/utils/cookies';

@Module({ name: 'auth', dynamic: true, store })
class AuthModule extends VuexModule {
  public token: string = getLocalToken() || getToken() || '';
  public loggedIn = false;
  public loginError = false;
  public user: IUser | null = null;

  // Getters
  get roles(): string[] {
    if (this.user !== null) {
      return this.user.roles.map(role => role.name);
    }
    return [];
  }

  get isActiveUser(): boolean {
    if (this.loggedIn && this.user) {
      return this.user.isActive;
    }
    return false;
  }

  // Mutations
  @Mutation
  private SET_TOKEN(token: string) {
    this.token = token;
    if (token !== '') {
      saveLocalToken(token);
      setToken(token);
    } else {
      removeLocalToken();
      removeToken();
    }
  }

  @Mutation
  private SET_LOGGED_IN(value: boolean) {
    this.loggedIn = value;
  }

  @Mutation
  private SET_LOGIN_ERROR(value: boolean) {
    this.loginError = value;
  }

  @Mutation
  private SET_USER(user: IUser | null) {
    this.user = user;
  }

  // Actions
  @Action
  public async CheckAuth(): Promise<boolean> {
    if (this.token !== '') {
      if (this.loggedIn) {
        return true;
      }

      let user: IUser | null;
      let loggedIn = false;
      try {
        user = await api.auth.testToken();
        loggedIn = true;
      } catch {
        user = null;
      }
      this.SET_LOGGED_IN(loggedIn);
      this.SET_LOGIN_ERROR(false);
      this.SET_USER(user);

      return loggedIn;
    }
    return false;
  }

  @Action
  public async Login(userInfo: { email: string; password: string }): Promise<boolean> {
    const email = userInfo.email.trim();
    const password = userInfo.password;

    let loggedIn = false;
    let loginError = false;
    try {
      const { accessToken } = await api.auth.loginAccessToken(email, password);
      if (accessToken) {
        this.SET_TOKEN(accessToken);
        loggedIn = true;
        await this.GetUserInfo();
      }
    } catch (err) {
      console.error(err);
      loginError = true;
    }

    this.SET_LOGGED_IN(loggedIn);
    this.SET_LOGIN_ERROR(loginError);

    return loggedIn;
  }

  @Action
  public async GetUserInfo() {
    if (this.token === '') {
      throw Error('GetUserInfo: Token not set')
    }
    const user = await api.user.readUserMe();
    this.SET_USER(user);
  }

  @Action
  public async Logout(): Promise<IMsg> {
    if (this.token === '') {
      throw Error("User is not logged in");
    }

    const msg = await api.auth.logout();

    resetRouter();
    this.SET_TOKEN('');
    this.SET_LOGGED_IN(false);
    this.SET_LOGIN_ERROR(false);
    this.SET_USER(null);

    return msg;
  }
}

export default getModule(AuthModule);

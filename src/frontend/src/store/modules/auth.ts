import {
  getModule,
  Module,
  Mutation,
  VuexModule,
  Action,
} from 'vuex-module-decorators';
import store from '@/store';

import api from '@/api';
import { IUser } from '@/api/schema/user';
import { getLocalToken, saveLocalToken } from '@/utils/jwt';

@Module({ name: 'auth', dynamic: true, store })
class AuthModule extends VuexModule {
  public token: string = getLocalToken() || '';
  public loggedIn = false;
  public loginError = false;
  public user: IUser | null = null;

  @Mutation
  private SET_TOKEN(token: string) {
    this.token = token;
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

  @Action
  public async Login(userInfo: { email: string; password: string }): Promise<boolean> {
    const email = userInfo.email.trim();
    const password = userInfo.password;

    let loggedIn = false;
    let loginError = false;
    let user: IUser | null = null;
    try {
      const { accessToken } = await api.auth.loginAccessToken(email, password);
      if (accessToken) {
        saveLocalToken(accessToken);
        this.SET_TOKEN(accessToken);
        user = await api.user.readUserMe();
        loggedIn = true;
      }
    } catch (err) {
      console.error(err);
      loginError = true;
    }

    this.SET_LOGGED_IN(loggedIn);
    this.SET_LOGIN_ERROR(loginError);
    this.SET_USER(user);

    return loggedIn;
  }

  get isLoggedIn() {
    return this.loggedIn;
  }
}

export default getModule(AuthModule);

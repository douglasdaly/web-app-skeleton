import { IName, INameCreate, INameUpdate } from './name';
import { IRole } from './role';


export interface IUserCreate {
  email: string;
  password: string;
  name?: INameCreate;
  roles?: string[];
  isActive?: boolean;
  isSuperuser?: boolean;
  isAdmin?: boolean;
}

export interface IUserUpdate {
  email?: string;
  password?: string;
  name?: INameUpdate;
  roles?: string[];
  isActive?: boolean;
  isSuperuser?: boolean;
  isAdmin?: boolean;
}

export interface IUser {
  uid: string;
  email: string;
  name?: IName;
  isActive: boolean;
  isSuperuser: boolean;
  isAdmin: boolean;
  roles: IRole[];
}

export default IUser;

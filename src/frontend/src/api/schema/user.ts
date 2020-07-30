import { IName, INameCreate, INameUpdate } from './name';

interface IUserBase {
  email?: string;
  isActive?: boolean;
  isSuperuser?: boolean;
  isAdmin?: boolean;
}

export interface IUserCreate extends IUserBase {
  email: string;
  password: string;
  name?: INameCreate;
}

export interface IUserUpdate extends IUserBase {
  password?: string;
  name?: INameUpdate;
}

export interface IUser extends IUserBase {
  uid?: string;
  name?: IName;
}

export default IUser;

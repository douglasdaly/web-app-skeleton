interface IRoleBase {
  description?: string;
}

export interface IRoleCreate extends IRoleBase {
  name: string;
}

export interface IRoleUpdate extends IRoleBase {
  name?: string;
}

export interface IRole extends IRoleBase {
  uid?: string;
  name: string;
}

export default IRole;

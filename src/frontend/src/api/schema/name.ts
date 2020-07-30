interface INameBase {
  title?: string;
  middle?: string;
  suffix?: string;
  preferred?: string;
}

export interface INameCreate extends INameBase {
  first: string;
  last: string;
}

export interface INameUpdate extends INameBase {
  first?: string;
  last?: string;
}

export interface IName extends INameBase {
  uid?: string;
  first: string;
  last: string;
}

export default IName;

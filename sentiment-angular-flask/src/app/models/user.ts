export class User {
  id!: number;
  public_id!: string;
  username!: string;
  name!: string;
  password!: string;
  email!: string;
  member!: boolean;
  token?: string;
}

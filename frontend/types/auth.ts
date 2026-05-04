export type AuthUser = {
  email: string;
  name: string;
  picture: string | null;
  first_name: string | null;
  last_name: string | null;
};

export type AuthSessionResponse = {
  authenticated: boolean;
  user: AuthUser | null;
};

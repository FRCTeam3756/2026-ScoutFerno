export type AuthUser = {
  email: string;
  name: string;
  picture: string | null;
  given_name: string | null;
  family_name: string | null;
};

export type AuthSessionResponse = {
  authenticated: boolean;
  user: AuthUser | null;
};

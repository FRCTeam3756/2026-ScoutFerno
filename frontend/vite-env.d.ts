/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly API_BASE_URL?: string;
  readonly GOOGLE_CLIENT_ID?: string;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}

type GoogleCredentialResponse = {
  credential?: string;
  select_by?: string;
};

type GoogleIdConfiguration = {
  client_id: string;
  callback: (response: GoogleCredentialResponse) => void | Promise<void>;
};

type GoogleButtonConfiguration = {
  theme?: "outline" | "filled_blue" | "filled_black";
  size?: "large" | "medium" | "small";
  text?:
    | "signin_with"
    | "signup_with"
    | "continue_with"
    | "signin";
  shape?: "rectangular" | "pill" | "circle" | "square";
  width?: number;
  type?: "standard" | "icon";
};

interface Window {
  google?: {
    accounts: {
      id: {
        initialize: (config: GoogleIdConfiguration) => void;
        renderButton: (
          parent: HTMLElement,
          options: GoogleButtonConfiguration
        ) => void;
        disableAutoSelect: () => void;
      };
    };
  };
}

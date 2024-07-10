/* eslint-disable react-refresh/only-export-components */
import { createContext, useContext, useEffect, useState } from "react";

type AccessKey = string | null;

type TokenProviderProps = {
  children: React.ReactNode;
  accessKey?: string;
  storageKey?: string;
};

type TokenProviderState = {
  key: AccessKey;
  setKey: (key: AccessKey) => void;
};

const initialState: TokenProviderState = {
  key: "",
  setKey: () => null,
};

const TokenProviderContext = createContext<TokenProviderState>(initialState);

export function TokenProvider({
  children,
  storageKey = "token",
  ...props
}: TokenProviderProps) {
  const [key, setKey] = useState<AccessKey>(() => localStorage.getItem(storageKey) || null);

  useEffect(() => {
    if (key) {
      localStorage.setItem(storageKey, key);
    } else {
      localStorage.removeItem(storageKey);
    }

  }, [key, storageKey]);

  const value = {
    key,
    setKey: (key: AccessKey) => {
      setKey(key);
    },
  };

  return (
    <TokenProviderContext.Provider value={value} {...props}>
      {children}
    </TokenProviderContext.Provider>
  );
}

export const useToken = () => {
  const context = useContext(TokenProviderContext);
  if (!context) {
    throw new Error("useToken must be used within a TokenProvider");
  }
  return context;
};

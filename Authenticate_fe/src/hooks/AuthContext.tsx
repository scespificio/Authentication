import { Loader } from "@/components/Loader";
import { toaster } from "@/components/ui/toaster";
import { ApiService } from "@/services/api";
import type { UserData } from "@/types/users";
import { createContext, useContext, useEffect, useRef, useState } from "react";
import { useNavigate } from "react-router";
import { useConfig } from "./ConfigContext";

interface AuthContextType {
  user?: UserData;
  login: (email: string, password: string) => Promise<void>;
  authorize: (host: string) => Promise<void>
  logout: () => void;
  tokenRefresh: () => void;
  apiService: ApiService;
}

const AuthContext = createContext<AuthContextType>({
  login: async () => { },
  authorize: async () => { },
  logout: () => { },
  tokenRefresh: () => { },
  apiService: new ApiService(),
});

interface Props {
  children: React.ReactNode;
}

export function AuthProvider(props: Props) {
  const navigate = useNavigate();
  const { updateConfig } = useConfig();
  const [loading, setLoading] = useState(true);
  const refreshingToken = useRef<boolean>(false);
  const [user, setUser] = useState<UserData | undefined>();

  const apiService = new ApiService(user);

  const handleLogin = async (email: string, password: string) => {
    setUser(await apiService.login(email, password));
    try {
      updateConfig(await apiService.getConfig());
    } catch {
      throw Error(
        "Une erreur est survenue lors du chargement de la configuration"
      );
    }
  };

  const handleAuthorization = async (host: string) => {
    await apiService.authorize(host);
  };

  const handleTokenRefresh = () => {
    if (!refreshingToken.current) {
      refreshingToken.current = true;
      apiService
        .refreshToken()
        .then((access) => setUser({ ...user!, access_token: access }))
        .catch(() => handleLogout("Votre session a expiré"))
        .finally(() => {
          refreshingToken.current = false;
        });
    }
  };

  const handleLogout = (message: string) => {
    setUser(apiService.logout());
    updateConfig();
    navigate("/connexion");
    toaster.create({
      description: message,
      type: "info",
    });
  };

  const value: AuthContextType = {
    user: user,
    login: handleLogin,
    authorize: handleAuthorization,
    tokenRefresh: handleTokenRefresh,
    logout: () => handleLogout("Vous êtes maintenant déconnecté"),
    apiService: apiService,
  };

  useEffect(() => {

    const storedUser = localStorage.getItem("user");
    if (storedUser) {
      setUser(JSON.parse(storedUser));
    }
    setLoading(false);
  }, []);

  useEffect(() => {

    if (user) {
      localStorage.setItem("user", JSON.stringify(user));
    } else {
      localStorage.removeItem("user");
    }
  }, [user]);

  if (loading) {
    return <Loader />;
  }
  return (
    <AuthContext.Provider value={value}>{props.children}</AuthContext.Provider>
  );
}

export const useAuth = () => {
  return useContext(AuthContext);
};

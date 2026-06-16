import { clientSystem, defaultSystem } from "@/components/ui/theme";
import type { ConfigData } from "@/types/users";
import { ChakraProvider, type SystemContext } from "@chakra-ui/react";
import { createContext, useContext, useEffect, useState } from "react";
import { Loader } from "@/components/Loader";

/* Configuration par défaut pour tests sans utilisateurs dans la DB */
interface ConfigContextType {
  config?: ConfigData;
  updateConfig: (config?: ConfigData) => void;
}

const ConfigContext = createContext<ConfigContextType>({
  updateConfig: () => {},
});

interface Props {
  children: React.ReactNode;
}

export function ConfigProvider(props: Props) {
  const [config, setConfig] = useState<ConfigData | undefined>();
  const [system, setSystem] = useState<SystemContext>(defaultSystem);
  const [loading, setLoading] = useState(true);

  const handleConfigUpdate = (config?: ConfigData) => {
    setConfig(config);
    setSystem(config && config.chakra ? clientSystem(config.chakra) : defaultSystem);
  };

  const value: ConfigContextType = {
    config: config,
    updateConfig: handleConfigUpdate,
  };

  useEffect(() => {
    const storedConfig = localStorage.getItem("config");
    if (storedConfig) {
      handleConfigUpdate(JSON.parse(storedConfig));
    }
    setLoading(false);
  }, []);

  useEffect(() => {
    if (config) {
      localStorage.setItem("config", JSON.stringify(config));
    } else {
      localStorage.removeItem("config");
    }
  }, [config]);

  return (
    <ConfigContext.Provider value={value}>
      <ChakraProvider value={system}>{ loading ? <Loader /> : props.children}</ChakraProvider>
    </ConfigContext.Provider>
  );
}

export const useConfig = () => {
  return useContext(ConfigContext);
};

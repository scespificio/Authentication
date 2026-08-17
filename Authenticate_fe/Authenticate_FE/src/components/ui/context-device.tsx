import { createContext, type ReactNode, useContext } from "react";
import { useMediaQuery } from "react-responsive";

type BreakpointContextType = {
  isDesktopOrLaptop: boolean;
  isTabletOrMobile: boolean;
};

const BreakpointContext = createContext<BreakpointContextType | null>(null);

const ContextDevice = ({ children }: { children: ReactNode }) => {
  const isDesktopOrLaptop = useMediaQuery({
    query: "(min-width: 1223px)",
  });

  const isTabletOrMobile = useMediaQuery({
    query: "(max-width: 1224px)",
  });

  return (
    <BreakpointContext.Provider
      value={{ isDesktopOrLaptop, isTabletOrMobile }}
    >
      {children}
    </BreakpointContext.Provider>
  );
};

export function useBreakpoint(): BreakpointContextType {
  const context = useContext(BreakpointContext);

  if (context === null) {
    throw new Error(
      "useBreakpoint doit être utilisé dans un ContextDevice",
    );
  }

  return context;
}

export default ContextDevice;
import React from 'react'
import { useMediaQuery } from "react-responsive";
import { createContext, useContext } from "react";

const BreakpointContext = createContext(null)

const ContextDevice = ({ children }) => {
    const isDesktopOrLaptop = useMediaQuery({ query: '(min-width: 1223px)' })
    const isTabletOrMobile = useMediaQuery({ query: '(max-width: 1224px)' })

    return (
        <BreakpointContext.Provider value={{ isDesktopOrLaptop, isTabletOrMobile }}>
            {children}
        </BreakpointContext.Provider>
    )
}

export function useBreakpoint() {
    return useContext(BreakpointContext);
}

export default ContextDevice
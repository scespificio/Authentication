import { Loader } from "@/components/Loader";
import { toaster } from "@/components/ui/toaster";
import { createContext, useContext, useEffect, useRef, useState } from "react";
import { useLocation } from "react-router";


interface HostContextType {
    host: string | undefined;
}

const HostContext = createContext<HostContextType>({
    host: undefined,
});

interface Props {
    children: React.ReactNode;
}

export function HostProvider(props: Props) {
    const [loading, setLoading] = useState(true);
    const [host, setHost] = useState(undefined);
    const location = useLocation();

    const value: HostContextType = { host };

    useEffect(() => {
        const params = new URLSearchParams(location.search)
        setHost(params.get("url") ?? undefined)
        setLoading(false);
    }, [location.search]);

    if (loading) {
        return <Loader />;
    }
    return (
        <HostContext.Provider value={value}>{props.children}</HostContext.Provider>
    );
}

export const useHost = () => {
    return useContext(HostContext);
};
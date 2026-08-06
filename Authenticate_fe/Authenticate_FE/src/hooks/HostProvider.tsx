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
        let extracted_url = params.get("url")

        if (extracted_url?.substring(0, 4) === "www.") { // reformats www
            let reformatted_url = extracted_url?.substring(4, extracted_url?.length + 1)
            console.log(reformatted_url)
            setHost(reformatted_url ?? undefined)
        } else {
            console.log(extracted_url)
            setHost(extracted_url ?? undefined)
        }

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
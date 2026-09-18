import type { React } from 'react';
import { Loader } from "@/components/Loader";
import type { DomainData } from "@/types/users";
import { createContext, useContext, useState, useEffect } from "react";
import { useAuth } from "@/hooks/AuthContext";
import { AxiosError } from "axios";
import { useErrorBoundary } from "react-error-boundary";

interface DomainContextType {
    domains?: DomainData;
}

const DomainContext = createContext<DomainContextType>({
});

interface Props {
    children: React.ReactNode;
}

export function DomainProvider(props: Props) {
    const { user, apiService } = useAuth();
    const { showBoundary } = useErrorBoundary();

    const [loading, setLoading] = useState(true);
    const [domains, setDomains] = useState<DomainData | undefined>();

    useEffect(() => {
        if (!user) {
            setLoading(false);
            return;
        }

        async function fetchData() {
            try {
                let response = await apiService.getUserDomains();
                setDomains(response)
            } catch (error: any) {
                if (error instanceof AxiosError && error.status === 401) {
                    showBoundary(error);
                }
            } finally {
                setLoading(false);
            }
        }
        fetchData();
    }, [user]);

    const value: DomainContextType = {
        domains: domains,
    };

    if (loading) {
        return <Loader />;
    }
    return (
        <DomainContext.Provider value={value}>{props.children}</DomainContext.Provider>
    );
}

export const useDomains = () => {
    return useContext(DomainContext);
};


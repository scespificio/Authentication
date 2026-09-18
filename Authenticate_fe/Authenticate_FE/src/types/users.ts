import type { SystemConfig } from "@chakra-ui/react";

export interface UserData {
    uid: number;
    email: string;
    username: string;
    first_name: string;
    last_name: string;
    access_token: string;
    refresh_token: string;
    sso_provider?: string;
    sso_subject?: string;
}

export interface ConfigData {
    appName: string;
    logo: string;
    email: {
        title: string;
        content: string;
        footer: string;
    }
    chakra?: SystemConfig;
}

export interface DomainData {
    nom: string;
    url: string;
}

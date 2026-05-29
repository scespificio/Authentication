import type { SystemConfig } from "@chakra-ui/react";

export interface UserData {
    uid: number;
    email: string;
    first_name: string;
    last_name: string;
    access_token: string;
    refresh_token: string;
    phone : string;
    brand : string;
    code : string;
    store_name : string;
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

import React from 'react'
import { createContext, useContext, useState, useEffect } from "react";
import Page from "@/components/Page";
import { useAuth } from "@/hooks/AuthContext";
import { useDomains } from "@/hooks/DomainContext";
import {
    Box,
    Button,
    Center,
    Flex,
    Heading,
    Image,
    Text,
} from "@chakra-ui/react";
import { Navigate } from "react-router";

const TestPage = () => {
    let domainsList = useDomains();

    useEffect(() => {
        if (error instanceof AxiosError && error.response?.status === 401) { // refresh if token expired
            tokenRefresh();
        } else {
            showBoundary(error);
        }
    } finally {
        setLoading(false);
    }
}, [user, apiService, tokenRefresh]);

return (
    <Page>

    </Page>
)
}

export default TestPage

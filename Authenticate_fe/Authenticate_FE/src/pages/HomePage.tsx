import Page from "@/components/Page";
import { useAuth } from "@/hooks/AuthContext";
import { Box, Button, Center, Flex, Heading, Image, Text } from "@chakra-ui/react";
import { AxiosError } from "axios";
import { useEffect, useState } from "react";
import { useErrorBoundary } from "react-error-boundary";
import { Navigate } from "react-router";

export default function HomePage() {
  const { showBoundary } = useErrorBoundary();
  const { user, tokenRefresh, apiService, logout } = useAuth();

  const [loading, setLoading] = useState<boolean>(true);
  const [domainsList, setDomainsList] = useState<any[]>([]);

  useEffect(() => {
    let ignore = false;

    async function fetchData() {
      try {
        if (!ignore) {
          setLoading(true);

          const [userRes] = await Promise.all([
            apiService.getUserDomains(),
          ]);

          if (!ignore) {
            setDomainsList(userRes);
          }
        }
      } catch (error: any) {
        if (!ignore) {
          if (error instanceof AxiosError && error.status === 401) {
            logout();
          } else {
            showBoundary(error);
          }
        }
      } finally {
        if (!ignore) {
          setLoading(false);
        }
      }
    }

    if (user) {
      fetchData();
    }

    return () => {
      ignore = true;
    };
  }, [apiService, tokenRefresh, showBoundary, logout, user]);

  const DOMAIN_STATUS_ICONS = {
    0: { src: "/images/cercle_vert.png", alt: "Statut : actif" },
    1: { src: "/images/cercle_violet.png", alt: "Statut : en attente" },
    2: { src: "/images/cercle_orange.png", alt: "Statut : inactif" },
  } as const;

  function getDomainStatusIcon(id: number) {
    return DOMAIN_STATUS_ICONS[(id % 3) as 0 | 1 | 2];
  }

  if (!user) {
    return <Navigate to="/connexion" replace />;
  }

  return (
    <Page>
      <Box background={{ lg: "white" }} py={4} p={{ lg: 8 }}>
        <Box>
          <Heading
            as="p"
            size={{ base: "4xl", lg: "5xl" }}
            lineHeight={{ lg: "100%" }}
            mb={8}
          >
            Bienvenue,{" "}
            <Text as="span" color="colorPalette.solid">
              {user.first_name}
            </Text>
          </Heading>

          <Text textStyle="xl" color="fg.muted">
            Vous êtes actuellement connecté(e) sur le compte :{" "}
            <Text
              as="span"
              color="colorPalette.solid"
              fontWeight="bold"
            >
              {user.email}
            </Text>
          </Text>
        </Box>
      </Box>

      <Box mt={10}>
        <Text textStyle="xl" mb={4} fontWeight="bold">
          Vos applications :
        </Text>

        <Flex direction="column" gap={3}>
          {domainsList.map((domain: any) => {
            const urlFull = `https://${domain.url}`;
            const icon = getDomainStatusIcon(domain.id);
            const domainName = domain.nom.split("/").slice(-1)[0];

            return (
              <Flex
                key={domain.id}
                align="center"
                gap={5}
                px={4}
                py={3}
              >
                <Image
                  src={icon.src}
                  alt={icon.alt}
                  width="50px"
                />

                <Text textStyle="xl" fontWeight="bold">
                  {domainName}
                </Text>

                <Box
                  borderLeftWidth="3px"
                  borderColor="border.solid"
                  alignSelf="stretch"
                />

                <a
                  href={urlFull}
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  <Text color="colorPalette.solid" textStyle="xl">
                    {domain.url}
                  </Text>
                </a>
              </Flex>
            );
          })}
        </Flex>

        <Center mt={8}>
          <Button onClick={logout} variant="outline">
            Se déconnecter
          </Button>
        </Center>
      </Box>
    </Page>
  );
}
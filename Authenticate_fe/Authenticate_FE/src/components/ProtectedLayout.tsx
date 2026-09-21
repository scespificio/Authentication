import { useAuth } from "@/hooks/AuthContext";
import { useConfig } from "@/hooks/ConfigContext";
import {
  Avatar,
  Text,
  Box,
  Image,
  Button,
  Container,
  Flex,
  Menu,
  Portal,
  Collapsible,
  useCollapsible,
} from "@chakra-ui/react";
import { LuMenu } from "react-icons/lu";
import { Link, useLocation } from "react-router";
import { Loader } from "@/components/Loader";
import { useDomains } from "@/hooks/DomainContext";

interface Props {
  children: React.ReactNode;
}

export default function ProtectedLayout(props: Props) {
  const { user, logout } = useAuth();
  const { config } = useConfig();
  const domainsList = useDomains();
  const location = useLocation();
  const collapsible = useCollapsible();
  const appName = import.meta.env.VITE_APP_NAME || "Authenticate";
  const brandName = config?.appName || "Authenticate";

  console.log("CONFIG !", config)
  if (!config) {
    return <Loader />;
  }

  return (
    <>

      <title>{`${appName} ${brandName}`}</title>
      <Box background="white">
        <Container height="64px">
          <Flex justify="space-between" align="center" height="full">
            <Link to="/">
              <Image
                src={`${import.meta.env.VITE_BACKEND_URL}${config!.logo}`}
                alt={`Logo ${config!.appName}`}
                height="40px"
              />
            </Link>
            <Flex justify="flex-end" gap={{ base: 1, lg: 5 }}>
              <Flex gap={5} align="center" fontSize="sm">
              </Flex>
              <Menu.Root>
                <Menu.Trigger asChild>
                  <Button variant="plain">
                    <Avatar.Root size="sm" shape="rounded">
                      <Avatar.Fallback name={user!.email} />
                    </Avatar.Root>
                  </Button>
                </Menu.Trigger>
                <Portal>
                  <Menu.Positioner>
                    <Menu.Content>
                      <Menu.Item value="logout" onClick={logout}>
                        Se déconnecter
                      </Menu.Item>
                    </Menu.Content>
                  </Menu.Positioner>
                </Portal>
              </Menu.Root>
            </Flex>
          </Flex>
        </Container>
      </Box>
      <Box background="colorPalette.solid" color="colorPalette.contrast">
        <Container>
          <Collapsible.RootProvider
            value={collapsible}
            hideFrom="lg"
            minH="40px"
          >
            <Flex
              gap={1}
              textTransform="uppercase"
              alignItems="center"
              height="40px"
            >
              <Collapsible.Trigger>
                <Collapsible.Indicator
                  transition="transform 0.2s"
                  _open={{ transform: "rotate(90deg)" }}
                >
                  <LuMenu size={18} />
                </Collapsible.Indicator>
              </Collapsible.Trigger>
              Menu
            </Flex>
            <Collapsible.Content textTransform="uppercase">
              <Flex direction="column" gap={2} textAlign="center" py={5}>
                <Link to="/" onClick={() => collapsible.setOpen(false)}>
                  Accueil
                </Link>
              </Flex>
            </Collapsible.Content>
          </Collapsible.RootProvider>
          <Flex
            height="40px"
            gap={5}
            justify="center"
            align="center"
            fontSize="sm"
            textTransform="uppercase"
            hideBelow="lg"
          >
            <>
              <Box as="span" color="colorPalette.muted">
                |
              </Box>
              {location.pathname === "/" ? (
                <Box as="span" fontWeight="bold">
                  Accueil
                </Box>
              ) : (
                <Box _hover={{ textDecoration: "underline" }} asChild>
                  <Link to="/">Accueil</Link>
                </Box>
              )}
              {domainsList.domains.map((domain) => {
                const urlFull = `https://${domain.url}`;
                const domainName = domain.nom.split("/").slice(-1)[0];

                return (
                  <>
                    <Box as="span" color="colorPalette.muted">
                      |
                    </Box>
                    <a
                      href={urlFull}
                      target="_blank"
                      rel="noopener noreferrer"
                    >
                      <Text >
                        {domainName}
                      </Text>
                    </a>
                  </>
                );
              })}
            </>
          </Flex>
        </Container>
      </Box>
      {props.children}
    </>
  );
}

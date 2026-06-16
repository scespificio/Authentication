import Page from "@/components/Page";
import { useAuth } from "@/hooks/AuthContext";
import { Box, Flex, Heading, Text } from "@chakra-ui/react";
import { AxiosError } from "axios";
import { useEffect, useState } from "react";
import { useErrorBoundary } from "react-error-boundary";

export default function HomePage() {

  const { showBoundary } = useErrorBoundary();
  const { tokenRefresh, apiService } = useAuth();
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    let ignore = false;
    async function fetchData() {
      try {
        if (!ignore) {
          setLoading(false);
        }
      } catch (error) {
        if (!ignore) {
          if (error instanceof AxiosError && error.status === 401) {
            tokenRefresh();
          } else {
            showBoundary(error);
          }
        }
      }
    }
    fetchData();
    return () => {
      ignore = true;
    };
  }, [apiService, tokenRefresh, showBoundary]);

  return (
    <Page>
      <Box background={{ lg: "white" }} borderRadius="xl" py={4} p={{ lg: 8 }}>
        <Flex justify="space-between" align="stretch" gap={5}>
          <Box>
            <Heading as="p" size={{ base: "4xl", lg: "5xl" }} lineHeight={{ lg: "100%" }} mb={8}>
              Bienvenue sur{" "}
              <Text as="span" color="colorPalette.solid">ROUTING ESPIFICIO</Text>
            </Heading>
          </Box>
        </Flex>
      </Box>
    </Page>
  );
}

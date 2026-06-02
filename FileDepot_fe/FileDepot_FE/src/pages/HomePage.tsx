import Page from "@/components/Page";
import { useAuth } from "@/hooks/AuthContext";
import { useConfig } from "@/hooks/ConfigContext";
import { Box, Flex, Heading, Text } from "@chakra-ui/react";
import { AxiosError } from "axios";
import { useEffect, useState } from "react";
import { useErrorBoundary } from "react-error-boundary";
import DragDrop from "@/components/DragDrop";

export default function HomePage() {

  const { showBoundary } = useErrorBoundary();
  const { tokenRefresh, apiService } = useAuth();
  const [loading, setLoading] = useState<boolean>(true);
  const [file, setFile] = useState(null);
  const [error, setError] = useState(null);

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

  const handleChange = (file) => {
    setFile(file);
  };

  const handleSubmit = async (e) => {
    e.preventDefault()

    try {
      const response = await apiService.postFileUpload(file)
      console.log(response)
    } catch (error) {
      if (error instanceof AxiosError) {
        switch (error.status) {
          case 401:
            tokenRefresh();
            break;
          default:
            setError(`Une erreur est survenue (${error.status}) : ${error.response.data.message[0]}`);
            break;
        }

      }
    }
  };

  const handleEmpty = () => {
    setFile(null)
  }

  return (
    <Page>
      <Box background={{ lg: "white" }} borderRadius="xl" py={4} p={{ lg: 8 }}>
        <Flex justify="space-between" align="stretch" gap={5}>
          <Box>
            <Heading as="p" size={{ base: "4xl", lg: "5xl" }} lineHeight={{ lg: "100%" }} mb={8}>
              Bienvenue sur{" "}
              <Text as="span" color="colorPalette.solid">File Depot</Text>
            </Heading>
          </Box>
        </Flex>
        <DragDrop file={file} error={error} handleChange={handleChange} handleEmpty={handleEmpty} handleSubmit={handleSubmit} />
      </Box>
    </Page>
  );
}

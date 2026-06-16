import BaseLayout from "@/components/BaseLayout";
import { Heading, Stack, Text } from "@chakra-ui/react";

export default function ErrorPage() {
  return (
    <BaseLayout>
      <Stack color="black" gap={0}>
        <Heading size="3xl">OUPS!</Heading>
        <Text fontSize="xl">Une erreur est survenue...</Text>
      </Stack>
    </BaseLayout>
  );
}

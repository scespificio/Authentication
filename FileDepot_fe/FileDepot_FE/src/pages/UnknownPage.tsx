import BaseLayout from "@/components/BaseLayout";
import { Heading, Stack, Text } from "@chakra-ui/react";

export default function UnknownPage() {
  return (
    <BaseLayout>
      <Stack color="black" gap={0}>
        <Heading size="3xl">OUPS!</Heading>
        <Text fontSize="xl">Cette page n'existe pas...</Text>
      </Stack>
    </BaseLayout>
  );
}

import type React from "react"
import BaseLayout from "@/components/BaseLayout";
import { Box, Heading, Text, Stack } from "@chakra-ui/react";

interface Props {
  title: string;
  subtitle: string;
  children: React.ReactNode;
}

export default function AccountLayout(props: Props) {
  return (
    <BaseLayout>
      <Box background="placeholder-background-name.gray" minW={{ lg: "xl" }} maxW={{ base: "5/6", lg: "2xl" }} borderRadius="3xl" p={8}>
        <Stack mb={10}>
          <Heading as="h1" size={{ base: "4xl", lg: "5xl" }}>
            {props.title}
          </Heading>
          <Text>{props.subtitle}</Text>
        </Stack>
        {props.children}
      </Box>
    </BaseLayout>
  );
}

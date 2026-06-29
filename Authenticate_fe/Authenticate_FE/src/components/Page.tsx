import { Box, Container } from "@chakra-ui/react";
import type React from "react";


interface Props {
  children?: React.ReactNode;
}

export default function Page({ children }: Props) {
  return (
    <>
      <Box
        backgroundImage="url('/images/placeholder-background-name.png')"
        backgroundSize="cover"
        position="absolute"
        width="full"
        height="full"
        opacity="0.4"
      ></Box>
      <Container mb={5} pt={{ base: 4, lg: 8 }}>
        {children}
      </Container>
    </>
  );
}

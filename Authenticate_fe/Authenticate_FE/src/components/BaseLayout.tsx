import type React from "react";
import { Box, Center, Image } from "@chakra-ui/react";
import { useBreakpoint } from "./ui/context-device";

interface Props {
  children: React.ReactNode;
}

export default function BaseLayout(props: Props) {

  const { isDesktopOrLaptop, isTabletOrMobile } = useBreakpoint();

  return (
    <Box
      backgroundImage="url('/placeholder-background-name.png')"
      backgroundSize="cover"
      position="absolute"
      width="full"
      height="full"
    >
      <Box position="absolute" top={0} left={5}>
        <Image src="/images/FAVICON ESPIFICIO.png" width={isDesktopOrLaptop ? "200px" : isTabletOrMobile ? "100px" : "100px"} alt="Logo placeholder" />
      </Box>
      <Center height="dvh">{props.children}</Center>
    </Box>
  );
}

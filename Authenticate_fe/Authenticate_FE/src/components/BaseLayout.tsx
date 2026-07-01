import { Box, Center, Image } from "@chakra-ui/react";

interface Props {
  children: React.ReactNode;
}

export default function BaseLayout(props: Props) {
  return (
    <Box
      backgroundImage="url('/placeholder-background-name.png')"
      backgroundSize="cover"
      position="absolute"
      width="full"
      height="full"
    >
      <Box position="absolute" top={0} left={5}>
        <Image src="/images/FAVICON ESPIFICIO.png" width="200px" alt="Logo placeholder" />
      </Box>
      <Center height="dvh">{props.children}</Center>
    </Box>
  );
}

import { Center, Spinner, VStack } from "@chakra-ui/react";

export function Loader() {
  return (
    <Center height="dvh">
      <VStack>
        Veuillez patienter...
        <Spinner />
      </VStack>
    </Center>
  );
}

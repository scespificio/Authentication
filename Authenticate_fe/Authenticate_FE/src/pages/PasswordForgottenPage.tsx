import { useState } from "react";
import { useErrorBoundary } from "react-error-boundary";
import { Link } from "react-router";

import {
  Box, Text,
  Button,
  Field,
  Fieldset,
  Input,
  Stack,
  Link as ChakraLink,
} from "@chakra-ui/react";

import AccountLayout from "@/components/AccountLayout";
import { ApiService } from "@/services/api";
import { AxiosError } from "axios";

export default function PasswordForgottenPage() {
  const [disabled, setDisabled] = useState<boolean>(true);
  const [loading, setLoading] = useState<boolean>(false);
  const [email, setEmail] = useState<string | null>();
  const [emailError, setEmailError] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [message, setMessage] = useState<string | null>(null);

  const { showBoundary } = useErrorBoundary();
  const apiService = new ApiService();

  function handleEmailChange(event: React.ChangeEvent<HTMLInputElement>) {
    setEmail(event.target.value);
    setEmailError(null);
    setError(null);
    setDisabled(!event.target.value);
  }

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setLoading(true);

    try {
      const response = await apiService.postPasswordForgotten(email!);
      setMessage(
        "Un email contenant un lien d'initialisation de votre mot de passe a été envoyé."
      );

    } catch (error) {
      if (error instanceof AxiosError) {
        const status = error.response?.status;

        switch (status) {
          case 400:
            if (error.response?.data?.email) {
              setEmailError(error.response.data.email[0]);
            }
            break;

          default:
            setError(
              `Une erreur est survenue (${status || error.code})`
            );
        }
      } else {
        showBoundary(error);
      }
    } finally {
      setLoading(false);
    }
  }

  return (
    <AccountLayout
      title="Mot de passe oublié"
      subtitle="Veuillez saisir une adresse mail associée à un compte existant et actif sur Authenticate."
    >
      <form onSubmit={handleSubmit}>
        <Fieldset.Root disabled={loading} mb={10}>
          <Fieldset.Content>
            <Field.Root invalid={!!emailError || !!error}>
              <Field.Label fontSize="md" fontWeight="bold" ps={3}>
                E-Mail
              </Field.Label>
              <Input
                type="email"
                background="bg"
                borderColor="template.gray"
                onChange={handleEmailChange}
                placeholder="Votre Adresse Mail"
              />
              {emailError && (
                <Field.ErrorText ps={3}>{emailError}</Field.ErrorText>
              )}
            </Field.Root>
          </Fieldset.Content>
        </Fieldset.Root>
        <Stack gap={3}>
          <Button
            type="submit"
            fontSize="md"
            fontWeight="bold"
            disabled={disabled}
            loading={loading}
          >
            Valider
          </Button>
          <Box textAlign="center">
            <ChakraLink asChild>
              <Link to="/connexion">Annuler</Link>
            </ChakraLink>
          </Box>
          <Text textAlign="center" color="primary" whiteSpace="pre-line"
            fontWeight="bold">
            {message}  </Text>
        </Stack>
      </form>
    </AccountLayout>
  );
}

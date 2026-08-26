import { useAuth } from "@/hooks/AuthContext";
import { useHost } from "@/hooks/HostProvider";
import { useState, useEffect } from "react";
import { useErrorBoundary } from "react-error-boundary";
import { Link, Navigate } from "react-router";

import { Box, Button, Field, Fieldset, Input, Stack, Link as ChakraLink, Separator } from "@chakra-ui/react";

import AccountLayout from "@/components/AccountLayout";
import { AxiosError } from "axios";

export default function LoginPage() {
  const [disabled, setDisabled] = useState<boolean>(true);
  const [loading, setLoading] = useState<boolean>(false);
  const [email, setEmail] = useState<string | null>();
  const [emailError, setEmailError] = useState<string | null>(null);
  const [password, setPassword] = useState<string | null>();
  const [error, setError] = useState<string | null>(null);
  const [authorized, setAuthorization] = useState<boolean>(false);

  const { user, login, authorize } = useAuth();
  const { host } = useHost();
  const { showBoundary } = useErrorBoundary();

  async function finishLogin(auth: string) {
    try {
      setLoading(true);
      await login(email!, password!, auth);
      await authorize(host);
      setAuthorization(true);

    } catch (error) {
      if (error instanceof AxiosError) {
        switch (error.status) {
          case 400:
            if (error.response?.data["email"]) {
              setEmailError(error.response.data["email"][0]);
            } else {
              setError("Identifiants ou droits d'accès invalides.");
            }
            break;
          case 401: {
            setError("Identifiants ou droits d'accès invalides.");
            break;
          }
          case 403: {
            setError("Vous n'avez pas les droits d'accès à ce domaine.");
            break;
          }
          case 404: {
            setError("URL introuvable.");
            break;
          }
          default:
            setError(`Une erreur est survenue (${error.status || error.code})`);
        }
      }
      else {
        showBoundary(error);
      }
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => { // handles SSO login
    const params = new URLSearchParams(location.search);
    const sso_authenticated = params.get("sso");

    if (sso_authenticated == "success") {
      finishLogin("sso");
    }

  }, [])

  useEffect(() => { // handles redirection
    if (user) { // check  si l'utilisateur est déjà dans le contexte & autorisé, redirige directement vers le domaine demandé
      if (host !== undefined && authorized) {
        window.location.replace(`https://${host}`)
      }
    }
  }, [user, host, authorized]);

  function handleEmailChange(event: React.ChangeEvent<HTMLInputElement>) {
    setEmail(event.target.value);
    setEmailError(null);
    setError(null);
    setDisabled(!event.target.value || !password);
  }

  function handlePasswordChange(event: React.ChangeEvent<HTMLInputElement>) {
    setPassword(event.target.value);
    setError(null);
    setDisabled(!email || !event.target.value);
  }

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    finishLogin("password");
  }

  const nextValue = (host ? `/connexion/?sso=success&url=${host}` : `/connexion/?sso=success`);

  if (user && host === undefined) { // aucun paramètre de recherche renseigné : l'utilisateur est redirigé à la page d'accueil.
    return <Navigate to="/" replace />;
  }

  return (
    <AccountLayout
      title="Bienvenue"
      subtitle="Veuillez saisir vos identifiants de connexion"
    >
      <Stack gap={3}>

        <form onSubmit={handleSubmit}>
          <Fieldset.Root disabled={loading} mb={10}>
            <Fieldset.Content gap={4}>
              <Field.Root invalid={!!emailError || !!error}>
                <Field.Label fontSize="md" fontWeight="bold" ps={3}>
                  Votre e-mail ou nom d'utilisateur
                </Field.Label>
                <Input
                  //type="email"
                  background="bg"
                  borderColor="template.gray"
                  onChange={handleEmailChange}
                  placeholder="Votre Adresse Mail"
                />
                {emailError && (
                  <Field.ErrorText ps={3}>{emailError}</Field.ErrorText>
                )}
              </Field.Root>
              <Field.Root invalid={!!error}>
                <Field.Label fontSize="md" fontWeight="bold" ps={3}>
                  Mot de passe
                </Field.Label>
                <Input
                  type="password"
                  background="bg"
                  borderColor="template.gray"
                  onChange={handlePasswordChange}
                  placeholder="Votre Mot de Passe"
                />
                <Field.ErrorText ps={3}>{error}</Field.ErrorText>
              </Field.Root>
            </Fieldset.Content>
          </Fieldset.Root>
          <Stack gap={4}>
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
                <Link to="/mot-de-passe-oublie">Mot de passe oublié ?</Link>
              </ChakraLink>
            </Box>
          </Stack>
        </form>
        <Separator />
        <Box textAlign="center">
          <Button
            type="submit"
            fontSize="md"
            fontWeight="bold"
            disabled={loading}
            loading={loading}
            onClick={() => { window.location.href = `/users/oidc/authenticate/?next=${encodeURIComponent(nextValue)}`; }}
          >
            Se connecter avec SSO
          </Button>
        </Box>
      </Stack>
    </AccountLayout>
  );
}

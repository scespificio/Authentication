import type React from "react";
import { useAuth } from "@/hooks/AuthContext";
import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { useErrorBoundary } from "react-error-boundary";

import { Stack, Input, Button, Text, Fieldset, Field } from "@chakra-ui/react";

import AccountLayout from "@/components/AccountLayout";
import { AxiosError } from "axios";
import { ApiService } from "@/services/api";

export default function ActivationPage() {
  const { uid, token } = useParams<{ uid: string; token: string }>();
  const apiService = new ApiService();

  const [status, setStatus] = useState<
    "loading" | "Validée" | "Erreur" | "Erreur réseau" | "Compte déjà activé"
  >("loading");

  const [email, setEmail] = useState("");

  const [isSending, setIsSending] = useState(false);
  const [message, setMessage] = useState<string | null>(null);
  const navigate = useNavigate();
  const [emailError, setEmailError] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const { user, login } = useAuth();
  const { showBoundary } = useErrorBoundary();
  const [disabled, setDisabled] = useState<boolean>(true);

  useEffect(() => {
    window.scrollTo({ top: 0, behavior: "smooth" });
    const activateAccount = async () => {
      try {
        const response = await apiService.postActivation(uid!, token!);
        setStatus("Validée");
        setMessage(
          "Un email contenant votre un lien d'initialisation de votre mot de passe a été envoyé"
        );
      } catch (error: any) {
        if (error instanceof AxiosError) {
          const status = error.response?.status;

          if (!status) {
            // Aucune réponse → probablement un souci réseau ou CORS
            setStatus("Erreur réseau");
            setMessage(
              "Seveur injoignable. Vérifier votre connexion Internet ou réessayer ulterieurement"
            );
            return;
          }

          if (status === 403) {
            setStatus("Compte déjà activé"); // Compte déjà activé
            setMessage(
              "Patientez nous vous redirigeans vers la page de connexion"
            );
            const delay = (ms: number) =>
              new Promise((res) => setTimeout(res, ms));
            await delay(3000);
            navigate("/", { replace: true });
          } else {
            setStatus("Erreur");
          }
        } else {
          setStatus("Erreur");
        }
      }
    };
    activateAccount();
  }, [uid, token]);

  function handleEmailChange(event: React.ChangeEvent<HTMLInputElement>) {
    setEmail(event.target.value);
    setEmailError(null);
    setError(null);
    setDisabled(!event.target.value);
  }

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    try {
      setLoading(true);
    } catch (error: any) {
      if (error instanceof AxiosError) {
        switch (error.status) {
          case 400:
            if (error.response?.data["email"]) {
              setEmailError(error.response.data["email"][0]);
            }
            break;
          default:
            setError(`Une erreur est survenue (${error.status || error.code})`);
        }
      } else {
        showBoundary(error);
      }
    } finally {
      setLoading(false);
    }
  }

  if (["Validée", "Erreur réseau", "Compte déjà activé"].includes(status)) {
    return (
      <AccountLayout title="Activation de votre compte" subtitle={status}>
        <Text>{message}</Text>
      </AccountLayout>
    );
  }

  if (status === "Erreur") {
    const handleResendActivation = async () => {
      if (!email) {
        setMessage("Renseigner votre email.");
        return;
      }

      try {
        setIsSending(true);
        setMessage(null);
        await apiService.postResendActivation(email); // ⬅️ méthode à définir dans ton ApiService
        setMessage(
          "Un nouveau lien d’activation a été envoyé à votre adresse email."
        );
      } catch (error: any) {
        setMessage(
          "Une erreur est survenue. Vérifiez votre adresse ou réessayez plus tard."
        );
      } finally {
        setIsSending(false);
      }
    };
    return (
      <AccountLayout
        title="Activation de votre compte"
        subtitle="L'activation de votre compte est invalide. Votre lien à peut-être expiré. Renseigner votre email.Si vous êtes éligible vous recevrez un nouveau lien d'activation."
      >
        <form onSubmit={handleSubmit}>
          <Fieldset.Root disabled={loading} mb={10}>
            <Fieldset.Content>
              <Field.Root invalid={!!emailError || !!error}>
                <Field.Label fontSize="md" fontWeight="bold" ps={3}>
                  <Text>E-mail de votre compte</Text>
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
          <Button
            colorScheme="blue"
            onClick={handleResendActivation}
            loading={isSending}
          >
            Renvoyer le lien d’activation
          </Button>
          <Text>{message}</Text>
        </form>
      </AccountLayout>
    );
  }
}

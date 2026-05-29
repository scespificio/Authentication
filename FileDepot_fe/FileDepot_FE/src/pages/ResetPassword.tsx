import { useState, useEffect } from "react";
import { useNavigate, useParams } from "react-router-dom";
import {
  Box,
  Container,
  Text,
  Image,
  Heading,
  Button,
  CardBody,
  CardRoot,
  Fieldset,
  Field,
} from "@chakra-ui/react";
import { PasswordInput } from "@/components/ui/password-input"; // ✅ nouvelle API toast


import { ApiService } from "@/services/api";
import { AxiosError } from "axios";
import AccountLayout from "@/components/AccountLayout";

export default function ResetPassword() {
  const apiService = new ApiService();

  const [visible, setVisible] = useState(false);
  const [password, setPassword] = useState("");
  const [confirm, setConfirm] = useState("");
  const [message, setMessage] = useState("");
  const { uid, token } = useParams<{ uid: string; token: string }>();
  const navigate = useNavigate();

  useEffect(() => {
    window.scrollTo({ top: 0, behavior: "smooth" });
  }, []);

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    // Règles simples côté client (ajuste selon ta politique)
    if (!password || password.length < 8) {
      setMessage("Mot de passe trop court, 8 caractères minimum.");
      return;
    }
    if (password !== confirm) {
      setMessage("Les mots de passe saisis diffèrent");
      return;
    }
    if (!uid || !token) {
      setMessage("Lien invalide ou incomplet (uid/token manquants).");
      return;
    }
    if (password === confirm) {
      try {
        const response = await apiService.postResetPassword(
          uid,
          token,
          password
        );
        setMessage(response.detail);
        setTimeout(() => {
          navigate("/", { replace: true });
        }, 2000);
      } catch (error: unknown) {
        if (error instanceof AxiosError) {
          const status = error.response?.status;
          if (!status) {
            setMessage("erreur réseau");
          } else {
            const data = error.response?.data;
            let msg = "";
            if (typeof data === "object") {
              msg = data.new_password.join("\n");
            } else {
              msg = "Erreur inconnue";
            }
            setMessage(msg);
          }
        }
      }
    }
  };

  return (

    <AccountLayout      
      title="Initialiser votre mot de passe"
      subtitle="Veuillez saisir et confirmer votre mot de passe"
    >

      <form onSubmit={handleSubmit}>
        <Fieldset.Root>
          <Field.Root required>
            <Field.Label>Nouveau mot de passe</Field.Label>
              <PasswordInput
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                visible={visible}
                onVisibleChange={setVisible}
                autoComplete="new-password"
                name="new-password"
              />
                </Field.Root>
                <Field.Root required>
                  <Field.Label>Confirmer le mot de passe</Field.Label>
                  <PasswordInput
                    value={confirm}
                    onChange={(e) => setConfirm(e.target.value)}
                    autoComplete="new-password"
                    name="new-password"
                  />
                </Field.Root>
              </Fieldset.Root>

              <Button type="submit" colorScheme="orange" w="full" mt={4}>
                Réinitialiser
              </Button>
              <Text textAlign="center" color="primary" whiteSpace="pre-line"
  fontWeight="bold">
              <br />
              <b>{message}</b> </Text>
        </form>
    </AccountLayout>
  );
}

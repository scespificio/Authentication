import { useAuth } from "../hooks/AuthContext";
import { Navigate, useLocation } from "react-router";

interface Props {
  children: React.ReactNode;
}

export default function ProtectedRoute(props: Props) {
  const { user } = useAuth();
  const location = useLocation();

  return user ? (
    props.children
  ) : (
    <Navigate to="/connexion" replace state={{ from: location }} />
  );
}

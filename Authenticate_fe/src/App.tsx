import type React from "react";
import { ErrorBoundary } from "react-error-boundary";
import { BrowserRouter, Outlet, Route, Routes, useLocation } from "react-router";
import { useLayoutEffect } from "react";

import ProtectedRoute from "@/components/ProtectedRoute";
import { Toaster } from "@/components/ui/toaster";
import ContextDevice from "@/components/ui/context-device";
import ProtectedLayout from "@/components/ProtectedLayout";

import { ConfigProvider } from "@/hooks/ConfigContext";
import { AuthProvider } from "@/hooks/AuthContext";
import { HostProvider } from "./hooks/HostProvider";

import AccountActivationPage from "@/pages/AccountActivationPage";
import LoginPage from "@/pages/LoginPage";
import PasswordForgottenPage from "@/pages/PasswordForgottenPage";
import HomePage from "@/pages/HomePage";
import ErrorPage from "@/pages/ErrorPage";
import UnknownPage from "@/pages/UnknownPage";
import ResetPassword from "@/pages/ResetPassword";

// Required because ScrollRestoration only works with React Router data mode
const ScrollToTopWrapper = ({ children }: { children: React.ReactNode }) => {
  const location = useLocation();

  useLayoutEffect(() => {
    window.scrollTo({ top: 0, left: 0, behavior: 'instant' });
  }, [location.pathname]);

  return children;
};

function App() {
  const appName = import.meta.env.VITE_APP_NAME || "Authenticate";

  return (
    <ContextDevice>
      <ConfigProvider>
        <title>{appName}</title>
        <ErrorBoundary fallback={<ErrorPage />}>
          <BrowserRouter>
            <HostProvider>
              <AuthProvider>
                <ScrollToTopWrapper>
                  <Routes>
                    {/* Public routes */}
                    <Route path="/activate/:uid/:token" element={<AccountActivationPage />} />
                    <Route
                      path="/reset-password/:uid/:token"
                      element={<ResetPassword />}
                    />
                    <Route path="connexion/" element={<LoginPage />} />
                    <Route
                      path="mot-de-passe-oublie"
                      element={<PasswordForgottenPage />}
                    />
                    {/* Zone protégée */}
                    <Route path="/">
                      <Route
                        element={
                          <ProtectedRoute>
                            <ProtectedLayout>
                              <Outlet />
                            </ProtectedLayout>
                          </ProtectedRoute>
                        }
                      >
                        <Route index element={<HomePage />} />
                      </Route>
                    </Route>
                    <Route path="*" element={<UnknownPage />} />
                  </Routes>
                  <Toaster />
                </ScrollToTopWrapper>
              </AuthProvider>
            </HostProvider>
          </BrowserRouter>
        </ErrorBoundary>
      </ConfigProvider>
    </ContextDevice>
  );
}

export default App;

/// <reference types="node" />

import { defineConfig, loadEnv, type UserConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tsconfigPaths from 'vite-tsconfig-paths'

// Typage des variables d'environnement
type AppEnv = {
  VITE_APP_BASE?: string
  ALLOWED_HOST?: string
  [key: string]: string | undefined
}

export default defineConfig(({ mode }): UserConfig => {
  // Charge les env (VITE_*, ALLOWED_HOST, etc.)
  const env = loadEnv(mode, process.cwd(), '') as AppEnv

  // Base publique (souvent "/")
  const base = env.VITE_APP_BASE ?? '/'

  // Gestion des hosts autorisés en dev (ne sert pas en prod)
  const allowedHosts = env.ALLOWED_HOST
    ? env.ALLOWED_HOST.split(',')
      .map((host) => host.trim())
      .filter(Boolean)
    : ['localhost']

  return {
    base,
    plugins: [react(), tsconfigPaths()],

    // ❗ Cette section est utilisée uniquement en DEV
    server: {
      host: true,
      port: 880, // Port DEV uniquement
      strictPort: true,
      allowedHosts,
    },

    // Build utilisé en PROD -> pas de port ici
    build: {
      sourcemap: mode !== 'production',
    },

    define: {
      __APP_ENV__: JSON.stringify(mode),
    },
  }
})

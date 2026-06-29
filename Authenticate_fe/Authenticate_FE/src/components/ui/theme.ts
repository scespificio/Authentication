import { createSystem, defaultConfig, defineConfig, type SystemConfig, type SystemContext } from "@chakra-ui/react"

const borderRadius = "3xl"

export const config = defineConfig({
  globalCss: {
    html: {
      colorPalette: "primary",
      color: "{colors.espificio.black}"
    },
  },
  theme: {
    tokens: {
      fonts: {
        body: { value: "Outfit" },
        heading: { value: "Outfit" },
      },
      colors: {
        espificio: {
          black: { value: "#2D2D2D" },
          gray: { value: "#F4F4F4" },
          teal: {
            50: { value: "#E6F7F4" },
            100: { value: "#BEEAE0" },
            200: { value: "#8DD6C8" },
            300: { value: "#4DBFAA" },
            400: { value: "#1BAF8A" },
            500: { value: "#179678" },
            600: { value: "#127A62" },
            700: { value: "#0D5D4A" },
            800: { value: "#084232" },
            900: { value: "#03281E" },
            950: { value: "#011A13" },
          },
          coral: {
            50: { value: "#FDF0EC" },
            100: { value: "#FAD9CE" },
            200: { value: "#F5B49F" },
            300: { value: "#EE8A6E" },
            400: { value: "#E8724A" },
            500: { value: "#D45A32" },
            600: { value: "#AA4726" },
            700: { value: "#80341B" },
            800: { value: "#582210" },
            900: { value: "#361308" },
            950: { value: "#220B04" },
          },
          purple: {
            50: { value: "#F0EAF7" },
            100: { value: "#D9CBEC" },
            200: { value: "#B59DD8" },
            300: { value: "#8D6DC0" },
            400: { value: "#6B3FA0" },
            500: { value: "#5A3388" },
            600: { value: "#48286E" },
            700: { value: "#361D54" },
            800: { value: "#25123A" },
            900: { value: "#160922" },
            950: { value: "#0D0516" },
          },
        },
      }
    },
    semanticTokens: {
      colors: {
        primary: {
          solid: { value: "{colors.espificio.teal.400}" },
          contrast: { value: "white" },
          fg: { value: "{colors.espificio.black}" },
          muted: { value: "{colors.espificio.teal.200}" },
          subtle: { value: "{colors.espificio.teal.100}" },
          emphasized: { value: "{colors.espificio.teal.300}" },
          focusRing: { value: "{colors.espificio.teal.400}" },
        },
        secondary: {
          solid: { value: "{colors.espificio.coral.400}" },
          contrast: { value: "white" },
          fg: { value: "{colors.espificio.black}" },
          muted: { value: "{colors.espificio.coral.200}" },
          subtle: { value: "{colors.espificio.coral.100}" },
          emphasized: { value: "{colors.espificio.coral.300}" },
          focusRing: { value: "{colors.espificio.coral.400}" },
        },
        tertiary: {
          solid: { value: "{colors.espificio.purple.400}" },
          contrast: { value: "white" },
          fg: { value: "{colors.espificio.black}" },
          muted: { value: "{colors.espificio.purple.200}" },
          subtle: { value: "{colors.espificio.purple.100}" },
          emphasized: { value: "{colors.espificio.purple.300}" },
          focusRing: { value: "{colors.espificio.purple.400}" },
        },
      }
    },
    recipes: {
      button: {
        base: {
          borderRadius: borderRadius,
        }
      },
      input: {
        base: {
          borderRadius: borderRadius
        }
      }
    }
  }
}
)

export const defaultSystem = createSystem(defaultConfig, config)

export function clientSystem(clientConfig: SystemConfig): SystemContext {
  return createSystem(defaultConfig, config, clientConfig)
}
// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  devtools: { enabled: true },
  modules: ['@nuxthq/ui', '@nuxtjs/google-fonts'],
  alias: {
    "./runtimeConfig": "./runtimeConfig.browser"
  },
  vite: {
    define: {
      "window.global": {}
    }
  },
  googleFonts: {
    families: {
      "Inter": {
        wght: [100, 200, 300, 400, 500, 600, 700, 800, 900],
      }
    },
    useStylesheet: true,
  }
})

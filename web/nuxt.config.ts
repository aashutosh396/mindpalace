// mindpalace v3 GUI — SPA, statically generated, served by the Python daemon.
// Dev loop: `mindpalace serve --port 7777 --no-open` + `npm run dev` (proxies /api + /ws).
// Release: `npm run build:dist` → ../mindpalace/web_dist (shipped as package data).
export default defineNuxtConfig({
  ssr: false,
  devtools: { enabled: false },
  compatibilityDate: '2025-07-15',
  css: ['~/assets/css/main.css'],
  app: {
    head: {
      title: 'mindpalace',
      meta: [{ name: 'viewport', content: 'width=device-width, initial-scale=1' }],
      link: [{
        rel: 'icon',
        href: 'data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>🏛️</text></svg>'
      }]
    }
  },
  nitro: {
    devProxy: {
      '/api': { target: 'http://127.0.0.1:7777/api', changeOrigin: true },
      '/ws': { target: 'http://127.0.0.1:7777/ws', ws: true }
    }
  }
})

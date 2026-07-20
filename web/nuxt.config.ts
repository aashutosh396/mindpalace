// mindpalace v3 GUI — SPA, statically generated, served by the Python daemon.
// Dev loop: `mindpalace serve --port 7777 --no-open` + `npm run dev` (proxies /api + /ws).
// Release: `npm run build:dist` → ../mindpalace/web_dist (shipped as package data).
export default defineNuxtConfig({
  ssr: false,
  devtools: { enabled: false },
  compatibilityDate: '2025-07-15',
  devServer: { port: 3777 },   // pinned — 3000/3001 collide with other local apps
  css: ['~/assets/css/main.css'],
  app: {
    head: {
      title: 'mindpalace',
      meta: [{ name: 'viewport', content: 'width=device-width, initial-scale=1' }],
      link: [{
        rel: 'icon',
        href: 'data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 24 24%22 fill=%22none%22 stroke=%22%23151517%22 stroke-width=%221.8%22 stroke-linecap=%22round%22><path d=%22M4.5 20v-8.5a7.5 7.5 0 0 1 15 0V20%22/><path d=%22M9.5 20v-5a2.5 2.5 0 0 1 5 0v5%22/><path d=%22M2.5 20h19%22/></svg>'
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

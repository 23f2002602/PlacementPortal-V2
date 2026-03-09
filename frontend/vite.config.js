import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

/*
  vite.config.js
  ──────────────
  Vite is the build tool + dev server for the CLI method.

  CDN METHOD:   browser loads Vue from <script src="https://unpkg.com/vue">
  CLI METHOD:   npm installs Vue, Vite compiles everything

  KEY CONFIG:
  ──────────
  1. plugins: [vue()]
     Tells Vite how to compile .vue files (template → render function)

  2. resolve.alias  '@' → src/
     So anywhere in code:  import X from '@/components/X.vue'
     instead of:           import X from '../../components/X.vue'

  3. server.proxy
     In dev, frontend runs on port 5173, Flask on 5000.
     Any request to /api/... gets forwarded to Flask.
     This avoids CORS errors during development.
     In production, Flask serves the built frontend directly.
*/

export default defineConfig({
  plugins: [vue()],

  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src')
    }
  },

  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:5000',
        changeOrigin: true
      }
    }
  }
})

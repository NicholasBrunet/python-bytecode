import { defineConfig } from 'vite';
import { resolve } from 'path';

export default defineConfig({
  root: './',
  publicDir: './public',
  envPrefix: 'VITE_',
  build: {
    rollupOptions: {
      input: {
        // Explicitly registers both standalone asset endpoints
        main: resolve(__dirname, 'index.html'),
        panel: resolve(__dirname, 'panel.html')
      }
    }
  },
  server: {
    port: 3000,
    host: '0.0.0.0'
  }
});
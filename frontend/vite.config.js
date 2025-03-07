import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'
import { webserver_port } from '../../../sites/common_site_config.json'
import frappeui from 'frappe-ui/vite'

// https://vitejs.dev/config/
export default defineConfig({
	plugins: [vue(), frappeui()],
	server: {
		port: 8080,
    proxy: {
        '^/(app|login|api|assets|files)': {
          target: `http://localhost:${webserver_port}`,
          ws: true,
          router: function (req) {
            const site_name = req.headers.host.split(':')[0]
            return `http://${site_name}:${webserver_port}`
          },
        },
      },
      allowedHosts: ["ctf.local"]
	},
	resolve: {
		alias: {
			'@': path.resolve(__dirname, 'src'),
      "tailwind.config.js": path.resolve(__dirname, "tailwind.config.js"),
		},
	},
	build: {
		outDir: `../${path.basename(path.resolve('..'))}/public/frontend`,
		emptyOutDir: true,
		target: 'es2015',
    commonjsOptions: {
      include: [/tailwind.config.js/, /node_modules/],
    },
	},
	optimizeDeps: {
		include: ['frappe-ui > feather-icons', 'showdown', 'engine.io-client', 'tailwind.config.js'],
	},
})

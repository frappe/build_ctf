import path from 'path';
import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';
import proxyOptions from './proxyOptions';

// https://vitejs.dev/config/
export default defineConfig({
	plugins: [vue()],
	server: {
		port: 8080,
		host: '0.0.0.0',
		proxy: proxyOptions,
		allowedHosts: ["ctf.local"]
	},
	resolve: {
		alias: {
			'@': path.resolve(__dirname, 'src')
		}
	},
	build: {
		outDir: '../ctf/public/frontend',
		emptyOutDir: true,
		target: 'es2015',
	},
});

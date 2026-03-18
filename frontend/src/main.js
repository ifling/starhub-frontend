import {
	createSSRApp
} from "vue";
import App from "./App.vue";
import { API_BASE_URL } from "./utils/config";
export function createApp() {
	const app = createSSRApp(App);
	app.config.globalProperties.$apiBase = API_BASE_URL;
	return {
		app,
	};
}

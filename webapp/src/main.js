import { createApp } from 'vue';
import App from './App.vue';
import * as ElementPlusIconsVue from '@element-plus/icons-vue';
import ElementPlus from 'element-plus';

const app = createApp(App);

// 注册所有的 Element Plus 图标组件
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
    app.component(key, component);
}

// 挂载应用
app.use(ElementPlus);
app.mount('#app');

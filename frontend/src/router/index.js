import { createRouter, createWebHistory } from 'vue-router'
import Simulator from '../views/Simulator.vue'
import KnowledgeViewer from '../views/KnowledgeViewer.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      redirect: '/simulator'
    },
    {
      path: '/simulator',
      name: 'Simulator',
      component: Simulator
    },
    {
      path: '/knowledge',
      name: 'KnowledgeViewer',
      component: KnowledgeViewer
    }
  ]
})

export default router



/*
	possibilities:
		have a place bar at the top: 
			"navigation"
			"grocery list"
*/


import { createRouter, createWebHistory } from 'vue-router'

import { guests_routes } from './guests'

const router = createRouter({
	history: createWebHistory (import.meta.env.BASE_URL),
	routes: [
		...guests_routes,
		

		/*
			https://router.vuejs.org/guide/migration/#Removed-star-or-catch-all-routes
		*/		
		{ 
			path: '/:pathMatch(.*)*', 
			name: 'not-found', 
			component: () => import ('@/regions/not_found.vue')  
		}
	]
})

export default router

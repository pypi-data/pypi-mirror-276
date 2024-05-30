


/*
	import { APP } from '@/main.js'
*/

import '@/assets/main.css'

import { createApp } from 'vue'
import earth from '@/apps/Earth/scenery/planet/field.vue'

/*
	This course is started in this script.
*/
export async function start () {
	const app = createApp (earth)
	app.mount ('#app')
}











/*

*/
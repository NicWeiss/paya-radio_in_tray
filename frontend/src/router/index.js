import Vue from 'vue'
import Router from 'vue-router'

import Login from '@/components/manage/login/index'
import Player from '@/components/manage/player/index'

import Auth from '@/components/service/auth'


Vue.use(Router)


let router = new Router({
  mode: 'history',
  routes: [
    {
      path: '/login',
      name: 'Login',
      component: Login,
      meta: {
        onlyGuest: true
      }
    },
    {
      path: '/',
      name: 'Player',
      component: Player,
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '*',
      redirect: '/login'
    }
  ]
})

router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.onlyGuest)) {
    if (Auth.isAuthenticated()) {
      next('/')
      return
    }
  }
  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (Auth.isAuthenticated()) {
      next()
      return
    }
    next('/login')
  }

  next()
})

export default router;

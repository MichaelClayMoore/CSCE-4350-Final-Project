import Vue from 'vue'
import Router from 'vue-router'
import homePage from '@/components/homePage'
import container from '@/components/container'
import logIn from '@/components/logIn'
import signUp from '@/components/signUp'
import cart from '@/components/cart'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'container',
      component: container,
      children: [
        {
          path: '/',
          name: 'homePage',
          component: homePage
        },
        {
          path: '/logIn',
          name: 'logIn',
          component: logIn
        },
        {
          path: '/signUp',
          name: 'signUp',
          component: signUp
        },
        {
          path: '/cart',
          name: 'Cart',
          component: cart
        }
      ]
    }
  ]
})

import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    user: null,
    admin: false,
    cart: [],
    items: [],
    coupons: []
  },
  actions:{
    addUserToDb({commit, rootState}, payload) {
      return new Promise((resolve, reject) =>{
        axios.post('http://127.0.0.1:5000/addUserToDb', {
          params: {
            userData:{
              'email':payload['email'],
              'password':payload['hashedPassword'],
              'admin':payload['admin']
            }
          }
        }).then(response  => {
          resolve("added user to database")
        }, (err)  => {
         console.error(err)
        })
      })
    },
    logInUser({commit, rootState}, payload) {
      return new Promise((resolve, reject) =>{
        axios.get('http://127.0.0.1:5000/logInUser', {
          params: {
            userData:{
              'email':payload['email'],
              'password':payload['hashedPassword']
            }
          }
        }).then(response  => {
          if(response.data != 'no user')
          {
            const bcrypt = require('bcryptjs')
            if(bcrypt.compareSync(payload['password'],response.data['password']))
            {
              commit('setUser',response.data['user_id'])
              commit('setAdmin',response.data['admin'])
              resolve("logged in successfully")
            }
            else {
              console.error("This is a bad username/password")
              resolve("Failed to log in")
            }
          }
          else {
            console.error("This is a bad username/password")
            resolve("Failed to log in")
          }
        }, (err)  => {
         console.error(err)
        })
      })
    },
    getItemsFromDb({commit, rootState}) {
      return new Promise((resolve, reject) =>{
        axios.get('http://127.0.0.1:5000/getItemsFromDb', {} ).then(response  => {
          commit('setItems',response.data)
          resolve('retrieved items from the database successfully')
        }, (err)  => {
         console.error(err)
        })
      })
    },
    addItemToUserCart({commit, rootState}, item){
      if(rootState.user){
        return new Promise((resolve, reject) =>{
          axios.post('http://127.0.0.1:5000/addItemToUserCart', {
            params: {
              userId:rootState.user,
              itemId:item.item_id
              }
            }
          ).then(response  => {
            commit('addItemToCart',item)
            resolve('added item to cart successfully')
          }, (err)  => {
           console.error(err)
          })
        })
      }
      else {
        commit('addItemToCart',item)
      }
    },
    addItemToDatabase({commit, rootState, dispatch}, item){
      return new Promise((resolve, reject) =>{
        axios.post('http://127.0.0.1:5000/addItemToDatabase', {
          params: {
            item:item
            }
          }
        ).then(response  => {
          dispatch('getItemsFromDb').then(response => {
            if(response = 'retrieved items from the database successfully')
              resolve('bought items from user\'s cart successfully')
            else
              resolve('unable to buy items from user\'s cart')

          }, (err) => {
            console.error(err)
          })
        }, (err)  => {
         console.error(err)
        })
      })
    },
    getItemsFromUserCart({commit,rootState}){
      return new Promise((resolve, reject) =>{
        axios.get('http://127.0.0.1:5000/getItemsFromUserCart', {
          params: {
            userId:rootState.user,
            }
          }
        ).then(response  => {
          let listOfItems = response.data
          for(let x = 0; x < listOfItems.length; x +=1)
            commit('addItemToCart',listOfItems[x])

          resolve('retrieved items from user\'s cart successfully')
        }, (err)  => {
         console.error(err)
        })
      })
    },
    deleteItemFromUserCart({commit,rootState}, item){
      if(rootState.user){
        return new Promise((resolve, reject) =>{
          axios.post('http://127.0.0.1:5000/deleteItemFromUserCart', {
            params: {
              userId:rootState.user,
              cart: rootState.cart,
              itemId: item.item_id
              }
            }
          ).then(response  => {
            commit('deleteItemFromCart', item)
            resolve('deleted item from user\'s cart successfully')
          }, (err)  => {
           console.error(err)
          })
        })
      }
      else {
        commit('deleteItemFromCart', item)
      }
    },
    buyItemsInCart({commit,rootState, dispatch})
    {
      return new Promise((resolve, reject) =>{
        axios.post('http://127.0.0.1:5000/buyItemsInCart', {
          params: {
            userId:rootState.user,
            cart: rootState.cart
            }
          }
        ).then(response  => {
          dispatch('getItemsFromDb').then(response => {
            if(response = 'retrieved items from the database successfully')
              resolve('bought items from user\'s cart successfully')
            else
              resolve('unable to buy items from user\'s cart')

          }, (err) => {
            console.error(err)
          })
        }, (err)  => {
         console.error(err)
        })
      })
    },
    getCouponFromDatabase({commit, rootState}) {
      return new Promise((resolve, reject) =>{
        axios.get('http://127.0.0.1:5000/getCouponFromDatabase', {} ).then(response  => {
          commit('setCoupons',response.data)
          resolve('retrieved coupons from the database successfully')
        }, (err)  => {
         console.error(err)
        })
      })
    },
    addCouponToDatabase({commit, rootState, dispatch}, item)
    {
      return new Promise((resolve, reject) =>{
        axios.post('http://127.0.0.1:5000/addCouponToDatabase', {
          params: {
            coupon:item
            }
          }
        ).then(response  => {
          console.log(response.data)
          if(response.data != 'error')
          {
            dispatch('getCouponFromDatabase').then(response => {
              if(response = 'retrieved coupons from the database successfully')
              resolve('added coupon to database successfully')
              else
              resolve('unable to retreive coupon from database')

            }, (err) => {
              console.error(err)
            })
          }
          else {
            resolve('unable to add coupon to database')
          }
        }, (err)  => {
         console.error(err)
        })
      })
    }
  },
  mutations: {
    setUser(state, userId)
    {
      state.user = userId
    },
    setCoupons(state, coupons)
    {
      state.coupons = coupons
    },
    setAdmin(state, admin)
    {
      state.admin = admin
    },
    resetUser(state)
    {
      state.user = null
      state.cart = []
      state.admin = false

      state.items.forEach((element) => {
        element.quantity = 1;
      })
    },
    setItems(state, listOfItems)
    {
      state.items = listOfItems
    },
    addItemToCart(state, item)
    {
      let found = false
      state.cart.forEach( (element) => {
        if(element.name == item.name)
        {
          if(element.quantity != (element.total_amount))
          {
            element.quantity += 1;
            found = true;
          }
          else {
            console.error("Cant add item to cart because you already have all of them in cart")
            found = true;
          }
        }
      })
      if(!found){state.cart.push(item);}
    },
    setCart(state, listOfItems)
    {
      state.cart = listOfItems
    },
    resetCart(state)
    {
      state.cart = []
    },
    deleteItemFromCart(state, item)
    {
      if(state.cart[state.cart.indexOf(item)].quantity > 1)
      {
        state.cart[state.cart.indexOf(item)].quantity -= 1;
      }
      else {
        state.cart.splice(state.cart[state.cart.indexOf(item)],1);
      }
    }
  }
})

<template>
  <div>
    <v-toolbar app>
      <img :src="require('@/assets/unt-square.png')" :style="{'height':'80%'}" @click="test()"/>
      <v-toolbar-title class="headline text-uppercase" @click="routeToHomePage">
        <span>CSCE 4250 </span>
        <span class="font-weight-light">Class Project</span>
      </v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn v-if="!this.user" flat to="/logIn">
        <span class="mr-2" to="/logIn">Log In</span>
      </v-btn>
      <v-btn v-if="!this.user" flat to="/signUp">
        <span class="mr-2" to="/signUp">Sign Up</span>
      </v-btn>
      <v-btn v-if="this.user" flat @click="logOut">
        <span class="mr-2">Log out</span>
      </v-btn>
      <v-btn flat to="/cart">
        <span class="mr-2">cart ({{this.cart.length}})</span>
      </v-btn>
    </v-toolbar>
    <router-view/>
    <flash-message class="notifier"></flash-message>
  </div>
</template>

<script>
import {mapState} from 'vuex'

  export default {
    computed: {...mapState(['cart','itemCount','user'])},
    data: () => ({
      name: 'container',
    }),
    mounted(){
      this.$store.dispatch('getItemsFromDb')
      this.$store.dispatch('getCouponFromDatabase')
    },
    methods:
    {
      routeToHomePage()
      {
        this.$router.push("/")
      },
      logOut()
      {
        this.$store.commit('resetUser')
        this.$store.commit('resetCart')
        this.flashMessage.show({status: 'success', title: 'Successfully logged out', time: 1500})
      },
      test(){
        console.log("test")
      }
    }
  }
</script>

<style>

</style>

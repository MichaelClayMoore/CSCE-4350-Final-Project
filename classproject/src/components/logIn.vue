<template>
  <v-container>
    <v-layout
      text-xs-center
      justify-center
      wrap
    >
    <v-card color="" class="mx-auto" :style="{'width':'80%'}">
        <v-toolbar flat :style="{'color':'#ffffff','background-color':'#0b8643'}" class="headline text-uppercase">Log In</v-toolbar>
      <v-form>
        <v-card-text>
          <v-text-field label="Email Address" v-model="userEmail"></v-text-field>
          <v-text-field label="Password" type="password" v-model="userPassword"></v-text-field>
        </v-card-text>
      </v-form>
      <v-btn flat @click="logIn">Log In</v-btn>
    </v-card>
    </v-layout>
  </v-container>
</template>

<script>
import {mapState} from 'vuex'

  export default {
    computed: {...mapState(['user'])},
    data: () => ({
      name: 'logIn',
      userEmail: '',
      userPassword: ''
    }),
    methods:
    {
      hashPassword(passwordGiven){
        const bcrypt = require('bcryptjs')
        const SALT_FACTOR = 8;
        return bcrypt.hashSync(passwordGiven, SALT_FACTOR)
      },
      logIn(){
        let payload = {
          'email':this.userEmail,
          'password':this.userPassword,
          'hashedPassword':this.hashPassword(this.userPassword)
        }

        let context = this
        this.$store.dispatch('logInUser',payload).then(function () {
            if(context.user)
            {
              context.$store.dispatch('getItemsFromUserCart').then(function(){
                context.$router.push('/')
                context.flashMessage.show({status: 'success', title: 'Successfully logged in', time: 1500})
              })
            }
            else {
              context.flashMessage.show({status: 'error', title: 'bad username or password', time: 1500})
            }
        });
      }
    }
  }
</script>

<style>

</style>

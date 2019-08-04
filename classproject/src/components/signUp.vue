<template>
  <v-container>
    <v-layout
      text-xs-center
      justify-center
      wrap
    >
    <v-card color="" class="mx-auto" :style="{'width':'80%'}">
        <v-toolbar flat :style="{'color':'#ffffff','background-color':'#0b8643'}" class="headline text-uppercase">Sign Up</v-toolbar>
      <v-form>
        <v-card-text>
          <v-text-field label="Email Address" v-model="userEmail"></v-text-field>
          <v-text-field label="Password" type="password" v-model="userPassword"></v-text-field>
          <v-text-field label="Confirm Password" type="password" v-model="userConfirmPassword"></v-text-field>
          <v-checkbox v-model="userAdmin" label="Admin"></v-checkbox>
        </v-card-text>
      </v-form>
      <v-btn flat @click="signUp">Sign Up</v-btn>
    </v-card>
    </v-layout>
  </v-container>
</template>

<script>
  export default {
    data: () => ({
      name: 'logIn',
      userAdmin:false,
      userEmail: '',
      userPassword: '',
      userConfirmPassword: ''
    }),
    methods:
    {
      hashPassword(passwordGiven){
        const bcrypt = require('bcryptjs')
        const SALT_FACTOR = 8;
        return bcrypt.hashSync(passwordGiven, SALT_FACTOR)
      },
      signUp(){
        if(this.userPassword === this.userConfirmPassword)
        {
          let payload = {
            'email':this.userEmail,
            'hashedPassword':this.hashPassword(this.userPassword),
            'admin':this.userAdmin
          }

          let context = this
          this.$store.dispatch('addUserToDb',payload).then(function(response){
            if(response == 'added user to database')
            {
              context.flashMessage.show({status: 'success', title: 'Successfully signed up', time: 1500})
            }
          })
        }
      }
    }
  }
</script>

<style>

</style>

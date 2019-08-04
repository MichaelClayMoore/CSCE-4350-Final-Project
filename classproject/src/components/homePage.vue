<template>
  <div>

    <v-dialog v-model="addDialog">
      <v-card>
        <v-toolbar :style="{'color':'#ffffff','background-color':'#0b8643'}">
          <v-toolbar-title class="headline text-uppercase">
            <span>Add Item </span>
          </v-toolbar-title>
        </v-toolbar>
        <v-container>
          <v-card-actions>
            <v-form :style="{'width':'100%'}">
              <v-text-field label="Item Name" v-model="itemNameToAdd"></v-text-field>
              <v-text-field label="Description" v-model="itemDescriptionToAdd"></v-text-field>
              <v-text-field label="Quantity" v-model="itemQuantityToAdd"></v-text-field>
              <v-text-field label="Price" v-model="itemPriceToAdd"></v-text-field>
            </v-form>
          </v-card-actions>
          <v-layout justify-center>
            <v-btn :style="{'color':'#ffffff','background-color':'#0b8643'}" @click="addNewItem()">Add Item</v-btn>
          </v-layout>
        </v-container>
      </v-card>
    </v-dialog>

    <v-dialog v-model="couponDialog">
      <v-card>
        <v-toolbar :style="{'color':'#ffffff','background-color':'#0b8643'}">
          <v-toolbar-title class="headline text-uppercase">
            <span>Add coupon </span>
          </v-toolbar-title>
        </v-toolbar>
        <v-container>
          <v-card-actions>
            <v-form :style="{'width':'100%'}">
              <v-text-field label="Coupon Code" v-model="couponCodeToAdd"></v-text-field>
              <v-layout justify-center>
                <v-date-picker color="#0b8643" v-model="couponEndDateToAdd"></v-date-picker>
              </v-layout>
            </v-form>
          </v-card-actions>
          <v-layout justify-center>
            <v-btn :style="{'color':'#ffffff','background-color':'#0b8643'}" @click="addNewCoupon()">Add Coupon</v-btn>
          </v-layout>
        </v-container>
      </v-card>
    </v-dialog>

    <v-layout wrap column :style="{'margin':'2%', 'width':'96%'}">

      <v-card v-for="item in items" :style="{'margin-bottom':'16px'}">
        <v-layout row>
          <img :src="require('@/assets/placeholder.jpg')" :style="{'width':'200px','height':'200px'}">
          </img>
          <v-layout :style="{'height':'199px'}">
            <v-card flat :style="{'width':'100%'}">
              <v-card-text :style="{'color':'#ffffff','background-color':'#0b8643','height':'28%'}">{{item.name}}</v-card-text>
              <v-card-actions :style="{'height':'48%'}">{{item.description}}</v-card-actions>
              <v-divider/>
              <v-layout justify-start align-center row :style="{'height':'25%'}">
                <v-card-text :style="{'width':'85%'}">${{Number.parseFloat(item.price).toFixed(2)}}</v-card-text>
                <v-spacer/>
                <v-layout row justify-center align-center>
                  <v-card-text>Quantity: {{item.total_amount}}</v-card-text>
                  <v-btn :style="{'color':'#ffffff','background-color':'#0b8643'}" @click="addItemToCart(item)">Add to cart</v-btn>
                </v-layout>
              </v-layout>
            </v-card>
          </v-layout>
        </v-layout>
      </v-card>

      <v-layout justify-center v-if="admin">
        <v-btn :style="{'color':'#ffffff','background-color':'#0b8643'}" @click="addDialog = true">
          Add a new Item
        </v-btn>
        <v-btn :style="{'color':'#ffffff','background-color':'#0b8643'}" @click="couponDialog = true">
          Add a new coupon
        </v-btn>
      </v-layout>

    </v-layout>
  </div>
</template>

<script>
import {mapState} from 'vuex'

  export default {
    computed: {...mapState(['items','user','admin'])},
    data: () => ({
      name: 'homePage',
      addDialog: false,
      couponDialog: false,
      itemNameToAdd:'',
      couponCodeToAdd: '',
      couponEndDateToAdd: '',
      itemDescriptionToAdd:'',
      itemQuantityToAdd:0,
      itemPriceToAdd:0
    }),
    methods:
    {
      addItemToCart(item)
      {
        let context = this
        this.$store.dispatch('addItemToUserCart',item).then(function(response){
          console.log(response)
          if(response == 'added item to cart successfully')
          {
            context.flashMessage.show({status: 'success', title: 'Successfully added item to cart', time: 1500})
          }
        })

        if(!this.user){this.flashMessage.show({status: 'success', title: 'Successfully added item to cart', time: 1500})}
      },
      addNewItem()
      {
        let payload = {
          'name':this.itemNameToAdd,
          'description':this.itemDescriptionToAdd,
          'quantity':this.itemQuantityToAdd,
          'price':this.itemPriceToAdd
        }
        let context = this

        this.$store.dispatch('addItemToDatabase',payload).then(function(response){
          if(response == 'bought items from user\'s cart successfully')
          {
            context.addDialog = false;
            context.flashMessage.show({status: 'success', title: 'Successfully added item to database', time: 1500})
          }
        })
      },
      addNewCoupon()
      {
        let payload = {
          'code':this.couponCodeToAdd,
          'endDate':this.couponEndDateToAdd,
        }
        let context = this

        console.log(this.couponEndDateToAdd)

        this.$store.dispatch('addCouponToDatabase',payload).then(function(response){
          if(response == 'added coupon to database successfully')
          {
            context.couponDialog = false;
            context.flashMessage.show({status: 'success', title: 'Successfully added coupon to database', time: 1500})
          }
          else {
            context.flashMessage.show({status: 'error', title: 'Unable to add coupon to the database', time: 1500})
          }
        })
      }
    }
  }
</script>

<style>

</style>

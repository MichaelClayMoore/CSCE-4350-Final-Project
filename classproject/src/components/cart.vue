<template>
  <div>
      <v-card color="" class="mx-auto" :style="{'width':'95%', 'height':'95%', 'margin':'0px', 'margin-top':'2%'}">
        <v-toolbar flat :style="{'color':'#ffffff','background-color':'#0b8643'}" class="headline text-uppercase">cart</v-toolbar>
        <v-data-table
          :items="cart"
          :headers = "headers"
        >
        <template slot="items" slot-scope="props">
          <td class="text-xs-center">{{ (props.item.name).toLocaleString() }}</td>
          <td class="text-xs-center">{{props.item.quantity}}</td>
          <td class="text-xs-center">${{Number.parseFloat(props.item.price * props.item.quantity * couponAppliedDiscout).toFixed(2)}}</td>
          <td class="text-xs-center">
              <v-btn icon class="mx-0" @click="deleteItem(props.item)">
                <v-icon color="red">delete</v-icon>
              </v-btn>
              <v-btn icon class="mx-0" @click="addItem(props.item)">
                <v-icon color="green">add</v-icon>
              </v-btn>
          </td>
        </template>
        </v-data-table>
        <v-divider/>
        <v-card-actions>
          <v-text-field label="Coupon Code" v-model="couponCode" :style="{'width':'0.05%'}" v-on:keyup.enter="applyCoupon()"></v-text-field>
          <v-spacer/>
            <span :style="{'margin-right':'3%'}">${{Number.parseFloat(this.totalPrice * this.couponAppliedDiscout).toFixed(2)}}</span>
            <v-btn :style="{'color':'#ffffff','background-color':'#0b8643'}" @click="buyItems()">Buy Now</v-btn>
        </v-card-actions>
      </v-card>
  </div>
</template>

<script>
import {mapState} from 'vuex'

  export default {
    computed: {...mapState(['cart', 'coupons'])},
    data: () => ({
      visibleCart: [],
      totalPrice: 0.00,
      couponAppliedDiscout: 1.00,
      couponCode:'',
      headers: [
        {text: 'Name', align: 'center', value: 'name'},
        {text: 'Quantity', align: 'center', value: 'quantity'},
        {text: 'Price', align: 'center', value: 'price'},
        {text: 'Options', align: 'center', value: ''}
      ],
    }),
    watch:{
    },
    mounted(){
      this.calculatePrice()
    },
    methods:
    {
      deleteItem(itemGiven)
      {
        let context = this;
        this.$store.dispatch('deleteItemFromUserCart',itemGiven).then(
          function(response){
            context.calculatePrice();
            context.flashMessage.show({status: 'success', title: 'Successfully deleted item', time: 1500})
          }
        )

      },
      addItem(itemGiven)
      {
        let context = this
        this.$store.dispatch('addItemToUserCart',itemGiven).then(function(response){
          console.log(response)
          if(response == 'added item to cart successfully')
          {
            context.calculatePrice();
            context.flashMessage.show({status: 'success', title: 'Successfully added item to cart', time: 1500})
          }
        })

        if(!this.user){this.flashMessage.show({status: 'success', title: 'Successfully added item to cart', time: 1500})}
        context.calculatePrice();
      },
      calculatePrice()
      {
        this.totalPrice = 0;
        for(let x = 0; x < this.cart.length ; x += 1)
        {
          let currentItemValue = this.cart[x].price * this.cart[x].quantity
          this.totalPrice += currentItemValue
        }
      },
      buyItems()
      {
        if(this.cart.length != 0){
          let context = this
          this.$store.dispatch('buyItemsInCart').then(function(response){
            if(response = 'bought items from user\'s cart successfully')
            {
              context.$store.commit('resetCart')
              context.flashMessage.show({status: 'success', title: 'Successfully bought items', time: 1500})
            }
          })
        }
        else{
          this.flashMessage.show({status: 'error', title: 'There is no items to buy', time: 1500})
        }
      },
      applyCoupon()
      {
        let context = this
        let couponFound = false;
        this.coupons.forEach((element) => {
          if(element.code == context.couponCode)
          {
            context.couponAppliedDiscout = 0.75
            context.calculatePrice()
            couponFound = true;
          }
        })

        if(couponFound){this.flashMessage.show({status: 'success', title: 'coupon successfully applied', time: 1500})}
        else{this.flashMessage.show({status: 'error', title: 'no coupon found', time: 1500})}

      }
    }
  }
</script>

<style>

</style>

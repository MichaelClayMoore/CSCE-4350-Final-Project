<template>
  <v-card :style="{'margin-bottom':'16px'}">
    <v-layout row>
      <img :src="require('@/assets/placeholder.jpg')" :style="{'width':'200px','height':'200px'}">
      </img>
      <v-layout :style="{'height':'199px'}">
        <v-card flat :style="{'width':'100%'}">
          <v-card-text :style="{'color':'#ffffff','background-color':'#0b8643','height':'28%'}">{{itemGiven.name}}</v-card-text>
          <v-card-actions :style="{'height':'48%'}">{{itemGiven.description}}</v-card-actions>
          <v-divider/>
          <v-layout justify-start row :style="{'height':'25%'}">
            <v-card-text>${{Number.parseFloat(itemGiven.price).toFixed(2)}}</v-card-text>
            <v-btn :style="{'color':'#ffffff','background-color':'#0b8643'}" @click="addItemToCart(itemGiven)">Add to cart</v-btn>
          </v-layout>
        </v-card>
      </v-layout>
    </v-layout>
  </v-card>
</template>

<script>
  export default {
    props:['itemGiven'],
    data: () => ({
      name:'item_' + itemGiven.item_id
    })
  }
</script>

<style>

</style>

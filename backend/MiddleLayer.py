from storeDAO import storeDAO
from flask import jsonify
from decimal import Decimal
from itertools import zip_longest
import json, sys, math, copy

class StoreMiddleLayer:

    def __init__(self):
        self.storeDAO = storeDAO()

    def testConnection(self):
        return self.storeDAO.testConnection()

    def addUserToDb(self, userData):
        return self.storeDAO.addUserToDb(userData)

    def logInUser(self, userData):
        return self.storeDAO.logInUser(userData)

    def getItemsFromDb(self):
        return self.storeDAO.getItemsFromDb()

    def getCouponFromDatabase(self):
        return self.storeDAO.getCouponFromDatabase()

    def addItemToUserCart(self, userId, itemId):
        return self.storeDAO.addItemToUserCart(userId, itemId)

    def addItemToDatabase(self, item):
        return self.storeDAO.addItemToDatabase(item)

    def getItemsFromUserCart(self, userId):
        return self.storeDAO.getItemsFromUserCart(userId)

    def deleteItemFromUserCart(self, userId, cart, itemId):
        tempCart = [item['item_id'] for item in cart]
        tempCart.remove(itemId)
        return self.storeDAO.deleteItemFromUserCart(userId, tempCart)

    def buyItemsInCart(self, userId, cart):
        for item in cart:
            buyResponse = self.storeDAO.buyItem(item)

        return self.resetUserCart(userId)

    def resetUserCart(self, userId):
        return self.storeDAO.resetUserCart(userId)

    def addCouponToDatabase(self, coupon):
        return self.storeDAO.addCouponToDatabase(coupon)

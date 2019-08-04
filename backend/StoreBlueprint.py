from flask import Flask, jsonify, request, Blueprint, abort
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api
from flask_cors import CORS
import json
from MiddleLayer import StoreMiddleLayer
store_page = Blueprint('store_page', __name__)
storeController = StoreMiddleLayer()

@store_page.route('/testConnection', methods=['POST'])
def testConnection():
    return storeController.testConnection()


@store_page.route('/addUserToDb', methods=['POST'])
def addUserToDb():
    userData = request.get_json()['params']['userData']
    return storeController.addUserToDb(userData)


@store_page.route('/logInUser', methods=['GET'])
def logInUser():
    userData = eval(request.args.get('userData'))
    return storeController.logInUser(userData)


@store_page.route('/getItemsFromDb', methods=['GET'])
def getItemsFromDb():
    return storeController.getItemsFromDb()


@store_page.route('/getCouponFromDatabase', methods=['GET'])
def getCouponFromDatabase():
    return storeController.getCouponFromDatabase()


@store_page.route('/addItemToUserCart', methods=['POST'])
def addItemToUserCart():
    return storeController.addItemToUserCart(request.get_json()['params']['userId'], request.get_json()['params']['itemId'])


@store_page.route('/addItemToDatabase', methods=['POST'])
def addItemToDatabase():
    return storeController.addItemToDatabase(request.get_json()['params']['item'])


@store_page.route('/getItemsFromUserCart', methods=['GET'])
def getItemsFromUserCart():
    return storeController.getItemsFromUserCart(request.args.get('userId'))


@store_page.route('/deleteItemFromUserCart', methods=['POST'])
def deleteItemFromUserCart():
    return storeController.deleteItemFromUserCart(request.get_json()['params']['userId'], request.get_json()['params']['cart'], request.get_json()['params']['itemId'])


@store_page.route('/buyItemsInCart', methods=['POST'])
def buyItemsInCart():
    return storeController.buyItemsInCart(request.get_json()['params']['userId'], request.get_json()['params']['cart'])


@store_page.route('/addCouponToDatabase', methods=['POST'])
def addCouponToDatabase():
    return storeController.addCouponToDatabase(request.get_json()['params']['coupon'])

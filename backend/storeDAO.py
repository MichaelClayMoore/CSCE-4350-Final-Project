from databaseConnections import databaseConnection
import psycopg2, psycopg2.extras, json, bcrypt
from datetime import datetime
from item import item

class storeDAO:

    def __init__(self):
        try:
            self.connection = databaseConnection()
        except psycopg2.Error as error:
            try:
                print(error.pgerror)
                print("Couldn't connect to the database")
            finally:
                error = None
                del error

    def testConnection(self):
        if self.connection:
            return json.dumps(True)
        else:
            return json.dumps(False)

    def addUserToDb(self, userData):
        conn = self.connection.connectToDb()
        trans = conn.begin()
        cursor = conn.connection.cursor()
        query = "SELECT store_add_user( '" + str(userData['email']).lower() + "'::text, '" + str(userData['password']) + "'::text, '" + str(userData['admin']) + "'::text );"
        print('\nquery is: ', query, '\n')
        try:
            try:
                cursor.execute(query)
                trans.commit()
                cursor.close()
                return 'Successful'
            except psycopg2.Error as error:
                try:
                    trans.rollback()
                    print(error.pgerror)
                    return 'error'
                finally:
                    error = None
                    del error

        finally:
            conn.close()

    def addItemToUserCart(self, userId, itemId):
        conn = self.connection.connectToDb()
        trans = conn.begin()
        cursor = conn.connection.cursor()
        query = 'UPDATE carts SET items_in_cart =  array_append(items_in_cart,' + str(itemId) + ') WHERE user_id = ' + str(userId) + ';'
        print('\nquery is: ', query, '\n')
        try:
            try:
                cursor.execute(query)
                trans.commit()
                cursor.close()
                return 'Successful'
            except psycopg2.Error as error:
                try:
                    trans.rollback()
                    print(error.pgerror)
                    return 'error'
                finally:
                    error = None
                    del error

        finally:
            conn.close()

    def deleteItemFromUserCart(self, userId, cart):
        conn = self.connection.connectToDb()
        trans = conn.begin()
        cursor = conn.connection.cursor()
        query = 'UPDATE carts SET items_in_cart = ARRAY' + str(cart) + '::integer[] WHERE user_id = ' + str(userId) + ';'
        print('\nquery is: ', query, '\n')
        try:
            try:
                cursor.execute(query)
                trans.commit()
                cursor.close()
                return 'Successful'
            except psycopg2.Error as error:
                try:
                    trans.rollback()
                    print(error.pgerror)
                    return 'error'
                finally:
                    error = None
                    del error

        finally:
            conn.close()

    def logInUser(self, userData):
        conn = self.connection.connectToDb()
        trans = conn.begin()
        cursor = conn.connection.cursor(cursor_factory=(psycopg2.extras.DictCursor))
        query = "SELECT user_id,email,password,admin FROM users WHERE email='" + str(userData['email']).lower() + "';"
        print('\nquery is: ', query, '\n')
        try:
            try:
                cursor.execute(query)
                row = cursor.fetchone()
                trans.commit()
                cursor.close()
                if row:
                    return json.dumps(dict(row))
                else:
                    return 'no user'
            except psycopg2.Error as error:
                try:
                    trans.rollback()
                    print(error.pgerror)
                    return 'error'
                finally:
                    error = None
                    del error

        finally:
            conn.close()

    def getItemsFromDb(self):
        conn = self.connection.connectToDb()
        trans = conn.begin()
        cursor = conn.connection.cursor(cursor_factory=(psycopg2.extras.DictCursor))
        query = 'SELECT item_id,name,price,description,total_amount FROM items;'
        print('\nquery is: ', query, '\n')
        try:
            try:
                cursor.execute(query)
                rows = cursor.fetchall()
                listOfItems = []
                for row in rows:
                    if row['total_amount'] <= 0:
                        continue
                    tempItem = item(row['item_id'], row['name'], row['price'], row['description'], row['total_amount'])
                    listOfItems.append(tempItem.serialize())

                trans.commit()
                cursor.close()
                return json.dumps(listOfItems)
            except psycopg2.Error as error:
                try:
                    trans.rollback()
                    print(error.pgerror)
                    return 'error'
                finally:
                    error = None
                    del error

        finally:
            conn.close()

    def getCouponFromDatabase(self):
        conn = self.connection.connectToDb()
        trans = conn.begin()
        cursor = conn.connection.cursor(cursor_factory=(psycopg2.extras.DictCursor))
        query = 'SELECT coupon_id,code,end_date FROM coupons;'
        print('\nquery is: ', query, '\n')
        try:
            try:
                cursor.execute(query)
                rows = cursor.fetchall()
                listOfCoupons = []
                for row in rows:
                    listOfCoupons.append({'couponId':row['coupon_id'],
                     'code':row['code'],
                     'endDate':str(row['end_date'])})

                trans.commit()
                cursor.close()
                return json.dumps(listOfCoupons)
            except psycopg2.Error as error:
                try:
                    trans.rollback()
                    print(error.pgerror)
                    return 'error'
                finally:
                    error = None
                    del error

        finally:
            conn.close()

    def getItemsFromUserCart(self, userId):
        conn = self.connection.connectToDb()
        trans = conn.begin()
        cursor = conn.connection.cursor(cursor_factory=(psycopg2.extras.DictCursor))
        query = '\n        with counts as (select item,count(*) from carts, unnest(items_in_cart) as item where user_id = ' + userId + ' group by item)\n        select item_id,name,price,description,total_amount,count from items,counts,carts where carts.user_id = ' + userId + ' AND counts.item = item_id\n        '
        print('\nquery is: ', query, '\n')
        try:
            try:
                cursor.execute(query)
                rows = cursor.fetchall()
                listOfItems = []
                for row in rows:
                    tempItem = item(row['item_id'], row['name'], row['price'], row['description'], row['total_amount'])
                    for x in range(row['count']):
                        listOfItems.append(tempItem.serialize())

                trans.commit()
                cursor.close()
                return json.dumps(listOfItems)
            except psycopg2.Error as error:
                try:
                    trans.rollback()
                    print(error.pgerror)
                    return 'error'
                finally:
                    error = None
                    del error

        finally:
            conn.close()

    def addItemToDatabase(self, item):
        conn = self.connection.connectToDb()
        trans = conn.begin()
        cursor = conn.connection.cursor()
        query = "INSERT into items(name,description,price,total_amount) VALUES('" + str(item['name']) + "','" + str(item['description']) + "', " + str(item['price']) + ', ' + str(item['quantity']) + ');'
        print('\nquery is: ', query, '\n')
        try:
            try:
                cursor.execute(query)
                trans.commit()
                cursor.close()
                return 'Successful'
            except psycopg2.Error as error:
                try:
                    trans.rollback()
                    print(error.pgerror)
                    return 'error'
                finally:
                    error = None
                    del error

        finally:
            conn.close()

    def buyItem(self, item):
        conn = self.connection.connectToDb()
        trans = conn.begin()
        cursor = conn.connection.cursor()
        quantityLeft = item['total_amount'] - item['quantity']
        query = 'UPDATE items SET total_amount = (' + str(quantityLeft) + ') WHERE item_id = ' + str(item['item_id']) + ';'
        print('\nquery is: ', query, '\n')
        try:
            try:
                cursor.execute(query)
                trans.commit()
                cursor.close()
                return 'Successful'
            except psycopg2.Error as error:
                try:
                    trans.rollback()
                    print(error.pgerror)
                    return 'error'
                finally:
                    error = None
                    del error

        finally:
            conn.close()

    def resetUserCart(self, userId):
        conn = self.connection.connectToDb()
        trans = conn.begin()
        cursor = conn.connection.cursor()
        query = 'UPDATE carts SET items_in_cart = ARRAY[]::integer[] WHERE user_id = ' + str(userId) + ';'
        print('\nquery is: ', query, '\n')
        try:
            try:
                cursor.execute(query)
                trans.commit()
                cursor.close()
                return 'Successful'
            except psycopg2.Error as error:
                try:
                    trans.rollback()
                    print(error.pgerror)
                    return 'error'
                finally:
                    error = None
                    del error

        finally:
            conn.close()

    def addCouponToDatabase(self, coupon):
        conn = self.connection.connectToDb()
        trans = conn.begin()
        cursor = conn.connection.cursor()
        query = "INSERT INTO coupons(code,end_date) values('" + str(coupon['code']) + "', TO_TIMESTAMP('" + str(coupon['endDate']) + "','YYYY-MM-DD' ) );"
        print('\nquery is: ', query, '\n')
        try:
            try:
                cursor.execute(query)
                trans.commit()
                cursor.close()
                return 'Successful'
            except psycopg2.Error as error:
                try:
                    trans.rollback()
                    print(error.pgerror)
                    return 'error'
                finally:
                    error = None
                    del error

        finally:
            conn.close()

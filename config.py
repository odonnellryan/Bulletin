from peewee import MySQLDatabase

database = MySQLDatabase(host='127.0.0.1', user='root', password='', database='bulletin')
page_length = 10
company_name = "Test Company"
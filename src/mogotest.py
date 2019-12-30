import pymongo
uri = "mongodb://127.0.0.1:27017"

#Uri is address, so we need client that can connect to the uri
client = pymongo.MongoClient(uri)

# create a mongod common object
database = client['fullstack']
# from collections create a collection objec
collection = database['students']
# access the  particular colection as a cursor object ( maybe an iterator / or generator
# students = collection.find({})
# for student in students:
#     print(student)

# transition to list comprehension

students=[student['marks'] for student in collection.find({})]
print(students)
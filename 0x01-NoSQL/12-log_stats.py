#!/usr/bin/env python3

'''A Python module that provides stats about nginx'''

from pymongo import MongoClient

if __name__ == '__main__':
    '''Prints the log stats in the nginx collection'''

    # Connection to MongoDB
    with MongoClient('mongodb://localhost:27017') as con:
        collection = con.logs.nginx

        # Total log count
        total_logs = collection.estimated_document_count()
        print(f'{total_logs} logs')

        # Methods statistics
        methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
        print('Methods:')
        for req in methods:
            count = collection.count_documents({'method': req})
            print(f'\tmethods {req}: {count}')

        # Status check statistics
        status_logs = collection.count_documents({'method': 'GET', 'path': '/status'})
        print(f'{status_logs} status check')

import pickle
import time


class Cache:
    def __init__(self):
        self.cache = dict()
        try:
            with open('cache.txt', 'rb') as file:
                origin_cache = pickle.load(file)
                new_cache = dict()
                for k, v in origin_cache.items():
                    old_records = []
                    records_time = v[1]
                    list_of_records = v[0]
                    # clean records with overdue TTL
                    for record in list_of_records:
                        ttl = record[2]
                        if records_time + ttl < time.time():
                            old_records.append(record)
                    for rec in old_records:
                        list_of_records.remove(rec)
                    if list_of_records:
                        new_cache[k] = (list_of_records, records_time)
                self.cache = new_cache.copy()
        except IOError:
            with open('cache.txt', 'w') as file:
                print('CREATE CACHE')

    def add_record(self, name, type_ask, info):
        self.cache[(name, type_ask)] = (info, time.time())
        self.save()

    def get_record(self, key):
        old_records = []
        if key in self.cache:
            value = self.cache[key]
            records_time = value[1]
            list_of_records = value[0]
            for record in list_of_records:
                ttl = record[2]
                if records_time + ttl < time.time():
                    old_records.append(record)
            for old_rec in old_records:
                list_of_records.remove(old_rec)
            return list_of_records
        return None

    def save(self):
        with open('cache.txt', 'wb') as file:
            pickle.dump(self.cache, file)
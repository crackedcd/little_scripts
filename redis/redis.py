import sys
import redis


class REDIS_CONFIG():

    def __init__(self):
        self.__ip = "127.0.0.1"
        self.__port = 56379
        self.__database = 0
        self.__password = "PwdRds@333"

    def get_db_config(self):
        return {
                "ip": self.__ip,
                "port": self.__port,
                "database": self.__database,
                "password": self.__password,
                }

class REDIS_DB:

    def __init__(self, db_config):
        try:
            pool = redis.ConnectionPool(host=db_config["ip"], port=db_config["port"], db=db_config["database"], password=db_config["password"])
                                        # socket_timeout=None, connection_pool=None, charset='utf-8', errors='strict', decode_responses=False, unix_socket_path=None
            r = redis.StrictRedis(connection_pool=pool)
            self.__pipe = r.pipeline()
        except Exception as e:
            print("Error: %s" % e)
            sys.exit()

    def get(self, key_list):
        try:
            for key in key_list:
                self.__pipe.get(key)
            return self.__pipe.execute()
        except Exception as e:
            return ("Error: %s" % e)
            sys.exit()

    def set(self, kv_list):
        try:
            k_list = []
            for k in kv_list:
                k_list.append(k)
                self.__pipe.set(k, kv_list[k])
            if False not in self.__pipe.execute():
                return dict(zip(k_list, self.get(k_list)))
            else:
                return False
        except Exception as e:
            return ("Error: %s" % e)
            sys.exit()


if __name__ == "__main__":
    redis_conf = REDIS_CONFIG()
    redis_db = REDIS_DB(redis_conf.get_db_config())
    set_rslt1 = redis_db.set({"aaa": "hahaha", "bbb": "heiheihei", "ccc": "xixixxi"})
    set_rslt2 = redis_db.set({"ddd": "hahaha", "eee": "heiheihei", "fff": "xixixxi"})
    get_rslt = redis_db.get(["aaa", "fff"])
    print(get_rslt)


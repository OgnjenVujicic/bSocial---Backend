import logging
from ElasticSearch.es_service import connect_elasticsearch,start_consuming_thread


if __name__ == '__main__':
    es = connect_elasticsearch()
    if es is None:
        print("Cant initialize ElasticSearch")
        exit()
    logging.basicConfig(level=logging.ERROR)

    th1 = start_consuming_thread("users")
    th2 = start_consuming_thread("posts")
    th3 = start_consuming_thread("comments")

    th1.join()
    th2.join()
    th3.join()
    
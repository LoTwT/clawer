# 异步爬虫
# 多线程、线程池基础

import time
from threading import Thread
from multiprocessing.dummy import Pool

# 小明要下载10个视频
movies = ['movie1', 'movie2', 'movie3', 'movie4', 'movie5',
          'movie6', 'movie7', 'movie8', 'movie9', 'movie10']


def download_movie(movie):
    print(f'start downloading {movie}')
    time.sleep(1)  # 模拟下载电影需要的时间
    print(f'finished download {movie}')


# 同步
def run_sync():
    for movie in movies:
        download_movie(movie)


# 多线程
def run_thread():
    threads = []
    for movie in movies:
        thread = Thread(target=download_movie, args=(movie,))
        threads.append(thread)
        thread.start()

    # 告诉主线程，要等待子线程都执行完以后再继续后面的代码
    for thread in threads:
        thread.join()


# 线程池
def run_pool():
    with Pool(10) as pool:
        pool.map(download_movie, movies)


if __name__ == "__main__":
    start = time.time()
    # run_sync()  # 同步执行
    # run_thread()  # 多线程
    run_pool()  # 线程池
    end = time.time()

    print(f"用时：{end - start}")

import schedule
import time

def job():
    print("定期执行的任务")

# 设置每1分钟执行一次任务
schedule.every(1).minutes.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
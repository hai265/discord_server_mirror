import schedule

def job(mirror):
    print(mirror)

def main():
    schedule.every(2).seconds.do(job, mirror = "mirror")
    while True:
        schedule.run_pending()
main()
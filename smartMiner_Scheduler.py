#!/usr/bin/env python2.7

# To mock scheduler process

from apscheduler.schedulers.blocking import BlockingScheduler
import smartMiner_BTC

INTERVAL_MINUTES = 2

scheduler = BlockingScheduler()


def WTH_JOB():
    smartMiner_BTC.refreshTopCoin();


scheduler.add_job(smartMiner_BTC.WTH_JOB, 'interval', seconds=INTERVAL_MINUTES);

try:
    scheduler.start()
except (KeyboardInterrupt, SystemExit):
    pass

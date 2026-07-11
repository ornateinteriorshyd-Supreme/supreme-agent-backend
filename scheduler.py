import time
import schedule
from agents.marketing_agent import MarketingAgent
from agents.supreme_agent import SupremeAgent

def job_marketing_post():
    print("[24/7 Scheduler] Executing strict scheduled Marketing Post...")
    marketing = MarketingAgent()
    marketing.process_message("Execute daily luxury post on Instagram.")

def job_quality_check():
    print("[24/7 Scheduler] Supreme Agent executing routine health check...")
    supreme = SupremeAgent()
    supreme.orchestrate("System check.")

# Schedule tasks strictly on designated times
schedule.every().day.at("09:00").do(job_marketing_post)
schedule.every().day.at("18:00").do(job_marketing_post)
schedule.every(10).minutes.do(job_quality_check)

def run_24_7_scheduler():
    print("Initializing 24/7/365 Autonomous Agent Scheduler... Running continuously without any interruption.")
    while True:
        schedule.run_pending()
        time.sleep(1) # Micro-second precision sleep

if __name__ == "__main__":
    run_24_7_scheduler()

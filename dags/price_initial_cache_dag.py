from airflow import DAG
from airflow.decorators import task
import pendulum
from tasks.kis_cache_task import KISCacheTask
import asyncio
from tasks.kis.utils.period_div_code import PeriodDivCode
from tasks.kis.utils.date_util import *

local_tz = pendulum.timezone("Asia/Seoul")
now = pendulum.now("Asia/Seoul") 
start_date = now.subtract(days=1)

default_args = {
    'owner': 'airflow',
    'start_date': start_date, 
    'retries': 0,
    'catchup': False
}

# 일봉 DAG
with DAG(
    dag_id='daily_price_initial_cache_dag',
    default_args=default_args,
    tags=['kis', 'cache', 'initial-loading']
) as daily_dag:

    @task
    def fetch_and_cache_kis_data(market_div_code, stock_code, date_from, date_to, period_div_code, org_adj_price):
        async def async_fetch_and_cache():
            kis_cache_task = await KISCacheTask.create()
            return await kis_cache_task.fetch_and_cache_data(
                market_div_code, stock_code, date_from, date_to, period_div_code, org_adj_price
            )
        return asyncio.run(async_fetch_and_cache())

    date_from , date_to = get_redis_key_dates(PeriodDivCode.DAY, 4)
    
    get_kis_data_daily = fetch_and_cache_kis_data(
        market_div_code='J',
        stock_code='005930',
        date_from=date_from,  
        date_to=date_to,    
        period_div_code=PeriodDivCode.DAY.value,
        org_adj_price=0
    )
    
# 주봉 DAG
with DAG(
    dag_id='weekly_price_initial_cache_dag',
    default_args=default_args,
    tags=['kis', 'cache', 'initial-loading']
) as weekly_dag:

    @task
    def fetch_and_cache_kis_data(market_div_code, stock_code, date_from, date_to, period_div_code, org_adj_price):
        async def async_fetch_and_cache():
            kis_cache_task = await KISCacheTask.create()
            return await kis_cache_task.fetch_and_cache_data(
                market_div_code, stock_code, date_from, date_to, period_div_code, org_adj_price
            )
        return asyncio.run(async_fetch_and_cache())

    date_from , date_to = get_redis_key_dates(PeriodDivCode.WEEK, 80)

    get_kis_data_weekly = fetch_and_cache_kis_data(
                market_div_code='J',
                stock_code='005930',
                date_from=date_from,
                date_to=date_to,
                period_div_code=PeriodDivCode.WEEK.value,
                org_adj_price=0
    )
    
# 월봉 DAG
with DAG(
    dag_id='monthly_price_initial_cache_dag',
    default_args=default_args,
    tags=['kis', 'cache', 'initial-loading']
) as monthly_dag:

    @task
    def fetch_and_cache_kis_data(market_div_code, stock_code, date_from, date_to, period_div_code, org_adj_price):
        async def async_fetch_and_cache():
            kis_cache_task = await KISCacheTask.create()
            return await kis_cache_task.fetch_and_cache_data(
                market_div_code, stock_code, date_from, date_to, period_div_code, org_adj_price
            )
        return asyncio.run(async_fetch_and_cache())

    #2020.11-2024.11
    date_from , date_to = get_redis_key_dates(PeriodDivCode.MONTH, 4)

    get_kis_data_monthly = fetch_and_cache_kis_data(
                market_div_code='J',
                stock_code='005930',
                date_from=date_from,
                date_to=date_to,
                period_div_code=PeriodDivCode.MONTH.value,
                org_adj_price=0
    )

# 연봉 DAG
with DAG(
    dag_id='yearly_price_initial_cache_dag',
    default_args=default_args,
    tags=['kis', 'cache', 'initial-loading']
) as yearly_dag:

    @task
    def fetch_and_cache_kis_data(market_div_code, stock_code, date_from, date_to, period_div_code, org_adj_price):
        async def async_fetch_and_cache():
            kis_cache_task = await KISCacheTask.create()
            return await kis_cache_task.fetch_and_cache_data(
                market_div_code, stock_code, date_from, date_to, period_div_code, org_adj_price
            )
        return asyncio.run(async_fetch_and_cache())

    # 1985-2023
    date_from, date_to = get_redis_key_dates(PeriodDivCode.YEAR)

    get_kis_data_yearly = fetch_and_cache_kis_data(
            market_div_code='J',
            stock_code='005930',
            date_from=date_from,
            date_to=date_to,
            period_div_code=PeriodDivCode.YEAR.value,
            org_adj_price=0
    )
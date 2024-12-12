from airflow import DAG
from airflow.decorators import task
import pendulum
from tasks.kis_cache_task import KISCacheTask
import asyncio
from tasks.kis.utils.period_div_code import PeriodDivCode
from tasks.kis.utils.redis_key_date_utils import *
from airflow.utils.dates import days_ago

local_tz = pendulum.timezone("Asia/Seoul")
now = pendulum.now("Asia/Seoul") 

default_args = {
    'owner': 'airflow',
    'start_date': now.subtract(days=1),
    'retries': 0,
    'catchup': False
}

# 일봉 DAG
with DAG(
    dag_id='daily_price_periodic_cache_dag',
    default_args=default_args,
    schedule_interval='0 0 * * *',  # 매일 자정에 실행
    tags=['kis', 'cache', 'periodic-caching']
) as daily_dag:

    @task
    def fetch_and_cache_kis_data(market_div_code, stock_code, date_from, date_to, period_div_code, org_adj_price):
        async def async_fetch_and_cache():
            kis_cache_task = await KISCacheTask.create()
            return await kis_cache_task.fetch_and_cache_data(
                market_div_code, stock_code, date_from, date_to, period_div_code, org_adj_price
            )
        return asyncio.run(async_fetch_and_cache())

    new_date_from = get_daily_date_from(4)
    
    get_kis_data_daily = fetch_and_cache_kis_data(
        market_div_code='J',
        stock_code='005930',
        date_from=new_date_from,  
        date_to="{{ macros.ds_format(ds, '%Y-%m-%d', '%Y%m%d') }}",  
        period_div_code=PeriodDivCode.DAY.value,
        org_adj_price=0
    )

# 주봉 DAG
with DAG(
    dag_id='weekly_price_periodic_cache_dag',
    default_args=default_args,
    schedule_interval='0 0 * * 1',  # 매주 월요일 자정에 실행
    tags=['kis', 'cache', 'periodic-caching'],
) as weekly_dag:

    @task
    def fetch_and_cache_kis_data(market_div_code, stock_code, date_from, date_to, period_div_code, org_adj_price):
        async def async_fetch_and_cache():
            kis_cache_task = await KISCacheTask.create()
            return await kis_cache_task.fetch_and_cache_data(
                market_div_code, stock_code, date_from, date_to, period_div_code, org_adj_price
            )
        return asyncio.run(async_fetch_and_cache())

    date_from = get_weekly_date_from(80)

    get_kis_data_weekly = fetch_and_cache_kis_data(
                market_div_code='J',
                stock_code='005930',
                date_from=date_from,
                date_to="{{ macros.ds_format(ds, '%Y-%m-%d', '%Y%m%d') }}",
                period_div_code=PeriodDivCode.WEEK.value,
                org_adj_price=0
    )
    
# 월봉 DAG
with DAG(
    dag_id='monthly_price_periodic_cache_dag',
    default_args=default_args,
    schedule_interval='0 0 1 * *',  # 매월 1일 자정에 실행
    tags=['kis', 'cache', 'periodic-caching']
) as monthly_dag:

    @task
    def fetch_and_cache_kis_data(market_div_code, stock_code, date_from, date_to, period_div_code, org_adj_price):
        async def async_fetch_and_cache():
            kis_cache_task = await KISCacheTask.create()
            return await kis_cache_task.fetch_and_cache_data(
                market_div_code, stock_code, date_from, date_to, period_div_code, org_adj_price
            )
        return asyncio.run(async_fetch_and_cache())

    date_from = get_monthly_date_from(4)
    
    get_kis_data_monthly = fetch_and_cache_kis_data(
        market_div_code='J',
        stock_code='005930',
        date_from=date_from,
        date_to="{{ macros.ds_format(ds, '%Y-%m-%d', '%Y%m%d') }}",
        period_div_code=PeriodDivCode.MONTH.value,
        org_adj_price=0
    )

# 연봉 DAG
with DAG(
    dag_id='yearly_price_periodic_cache_dag',
    default_args=default_args,
    schedule_interval='0 0 1 1 *', # 매년 1월 1일 자정에 실행
    tags=['kis', 'cache', 'periodic-caching']
) as yearly_dag:

    @task
    def fetch_and_cache_kis_data(market_div_code, stock_code, date_from, date_to, period_div_code, org_adj_price):
        async def async_fetch_and_cache():
            kis_cache_task = await KISCacheTask.create()
            return await kis_cache_task.fetch_and_cache_data(
                market_div_code, stock_code, date_from, date_to, period_div_code, org_adj_price
            )
        return asyncio.run(async_fetch_and_cache())
    
    date_from = get_yearly_date_from()

    get_kis_data_yearly = fetch_and_cache_kis_data(
        market_div_code='J',
        stock_code='005930',
        date_from='{{ (execution_date - macros.dateutil.relativedelta.relativedelta(years=1)).strftime("%Y0101") }}',
        date_to="{{ macros.ds_format(ds, '%Y-%m-%d', '%Y%m%d') }}",
        period_div_code=PeriodDivCode.YEAR.value,
        org_adj_price=0
    )

from tasks.kis.dto.request import *
from tasks.kis.service.kis_rest_client import KoreaInvestRestClient
from infrastructure.redis_client import get_redis
import json

class KISCacheTask:
    def __init__(self, redis_client):
        self.redis_client = redis_client
        self.kis_client = KoreaInvestRestClient()

    @classmethod
    async def create(cls):
        redis_client = await get_redis()
        return cls(redis_client)

    async def fetch_and_cache_data(self, market_div_code, stock_code, date_from, date_to, period_div_code, org_adj_price):
        request = DailyItemChartPriceReq(
            marketDivCode=market_div_code,
            stockCode=stock_code,
            dateFrom=date_from,
            dateTo=date_to,
            periodDivCode=period_div_code,
            orgAdjPrice=org_adj_price
        )
        try:
            response = self.kis_client.get_daily_item_chart_price(request) 
            print(response)

            price_list = response['result'][1]
            print(price_list)

            cache_value = json.dumps(price_list)
            redis_key = f"{request.stockCode}:{request.periodDivCode}:{request.dateFrom}:{request.dateTo}"
            await self.redis_client.set(redis_key, cache_value) 
            
            return f"{date_from}-{date_to} 캐싱 성공 성공"
        
        except Exception as e:
            print(f"Error fetching data: {e}")
            raise


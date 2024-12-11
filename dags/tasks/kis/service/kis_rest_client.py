from tasks.kis.service.kis_invest_api import KoreaInvestApi
from tasks.kis.dto.request import *
import os
import requests
import json
from dags.config.config import settings

class KoreaInvestRestClient:  
    def get_daily_item_chart_price(self, request: DailyItemChartPriceReq):
        """국내 주식 기간별 시세 (일/주/월/년) API 요청.

            Note: 국내주식기간별시세(일/주/월/년)[v1_국내주식-016]
        """

        path = '/api/kis/stocks/daily/item-chart-price/origin'
        request_url = settings.flex_server+path

        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json'
        }

        try:
            request_dict = {
                "marketDivCode": request.marketDivCode,
                "stockCode": request.stockCode,
                "dateFrom": request.dateFrom,
                "dateTo": request.dateTo,
                "periodDivCode": request.periodDivCode,
                "orgAdjPrice": request.orgAdjPrice
            }
            response = requests.post(request_url, headers=headers, json=request_dict, timeout=10)
            print(request_dict)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise
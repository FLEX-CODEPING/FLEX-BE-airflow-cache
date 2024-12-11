from collections import namedtuple
import json
import requests
import pandas as pd
from tasks.kis.dto.response import *


class KoreaInvestApi:
    def __init__(self, config, base_headers):
        self.cust_type = config['cust_type']
        self._base_headers = base_headers
        self.is_paper_trading = config['is_paper_trading']
        self.using_url = config['using_url']

    def _transform_kis_response(self, url, tr_id, params, is_post_request=False, mappings=None):
        """KIS API 응답을 컬럼 필터링 및 변환합니다.

        Args:
            url (str): API 요청 URL
            tr_id (str): 거래 ID
            params (dict): API 요청 파라미터
            is_post_request (bool): POST 요청 여부
            mappings (dict): 매핑 규칙

        Returns:
            dict: 필터링 및 변환된 데이터
        """
        kis_response = self._fetch_kis_response(url, tr_id, params, is_post_request)
        
        if kis_response.is_ok():
            body = kis_response.get_body()
            
            if mappings is None:
                return body

            result = {}
            if hasattr(body, "output") and getattr(body, "output"):
                output_data = getattr(body, "output")

                if isinstance(output_data, dict):
                    output_data = [output_data]

                result = [
                    {mappings["output"].get(k, k): v for k, v in item.items() if k in mappings["output"]}
                    for item in output_data
                ]
                return result 

            for key in ["output1", "output2"]:
                if hasattr(body, key) and getattr(body, key):
                    output_data = getattr(body, key)

                    if isinstance(output_data, dict):
                        output_data = [output_data]

                    result[key] = [
                        {mappings[key].get(k, k): v for k, v in item.items() if k in mappings[key]}
                        for item in output_data
                    ]
            return result if result else body
        
    def _fetch_kis_response(self, api_url, tr_id, params, is_post_request=False):
        """KIS API를 호출하고 KisApiResponse 객체를 반환합니다.

        Args:
            api_url (str): API endpoint url
            tr_id (str): 거래 id
            params (dict): API parameters
            is_post_request (bool): POST 요청 여부

        Returns:
            KisApiResponse: KIS API 응답 객체
        """
        try:
            url = f"{self.using_url}{api_url}"
            headers = self._base_headers

            # 추가 Header 설정
            if tr_id[0] in ('T', 'J', 'C'):
                if self.is_paper_trading:
                    tr_id = 'V' + tr_id[1:]
            headers["tr_id"] = tr_id
            headers["custtype"] = self.cust_type

            if is_post_request:
                res = requests.post(url, headers=headers, data=json.dumps(params))
            else:
                res = requests.get(url, headers=headers, params=params)

            res.raise_for_status()
            
            return KisApiResponse(res) 

        except requests.RequestException as e:
            raise Exception(f"Request error occurred: {e}")
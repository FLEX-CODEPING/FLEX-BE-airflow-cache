from pydantic import BaseModel, Field
from typing import Literal

class DailyItemChartPriceReq(BaseModel):
    marketDivCode: Literal['J', 'ETF', 'ETN'] = Field(
        ...,
        description="시장 분류 코드. (J: 주식, ETF, ETN)"
    )  # 시장 분류 코드
    stockCode: str = Field(
        ...,
        description="종목 코드. (종목번호(6자리). ETN의 경우, Q로 시작 (ex. Q500001))"
    )  # 종목 코드
    dateFrom: str = Field(
        ...,
        description="조회 시작 날짜 (YYYYMMDD 형식). (ex. 20220501)"
    )  # 조회 시작 날짜
    dateTo: str = Field(
        ...,
        description=(
            "조회 종료 날짜 (YYYYMMDD 형식). "
            "주(W), 월(M), 년(Y) 봉 조회 시, 종료 날짜에 대한 조건:\n"
            "1. date_to 가 현재일 까지인 경우:\n"
            "  - 주봉 조회: 해당 주의 첫번째 영업일 포함되어야 함.\n"
            "  - 월봉 조회: 해당 월의 전월 일자로 시작되어야 함.\n"
            "  - 년봉 조회: 해당 년의 전년도 일자로 시작되어야 함.\n"
            "2. date_to 가 현재일보다 이전일인 경우:\n"
            "  - 주봉 조회: 해당 주의 첫번째 영업일 포함되어야 함.\n"
            "  - 월봉 조회: 해당 월의 영업일 포함되어야 함.\n"
            "  - 년봉 조회: 해당 년의 영업일 포함되어야 함."
        )
    )  # 조회 종료 날짜
    periodDivCode: Literal['D', 'W', 'M', 'Y'] = Field(
        ...,
        description="기간 분류 코드. (D: 일봉, W: 주봉, M: 월봉, Y: 년봉)"
    )  # 기간 분류 코드
    orgAdjPrice: Literal[0, 1] = Field(
        ...,
        description="수정주가 여부. (0: 수정주가, 1: 원주가)"
    )  # 수정주가 여부
class KisApiResponse:
    """KisApiResponse class 는 API 응답을 처리하고, 응답을 객체로 변환하여 헤더, 본문 등의 정보를 추출 및 관리합니다.

    Attributes:
        _res_code (int): 응답 상태 코드
        _resp (requests.Response): 원본 응답 객체
        _header (namedtuple): 응답 헤더 정보
        _body (namedtuple): 응답 본문 정보
        _err_code (str): 응답 에러 코드
        _err_message (str): 응답 에러 메시지
    """
    def __init__(self, resp):
        self._res_code = resp.status_code
        self._resp = resp
        self._header = self._set_header()
        self._body = self._set_body()
        self._err_code = self._body.rt_cd
        self._err_message = self._body.msg1

    def get_result_code(self):
        return self._res_code

    def _set_header(self):
        fld = dict()
        for x in self._resp.headers.keys():
            if x.islower():
                fld[x] = self._resp.headers.get(x)
        _th_ = namedtuple('header', fld.keys())
        return _th_(**fld)

    def _set_body(self):
        _tb_ = namedtuple('body', self._resp.json().keys())
        return _tb_(**self._resp.json())

    def get_header(self):
        return self._header

    def get_body(self):
        return self._body

    def get_response(self):
        return self._resp

    def is_ok(self):
        try:
            return self.get_body().rt_cd == '0'
        except:
            return False

    def get_error_code(self):
        return self._err_code

    def get_error_message(self):
        return self._err_message

    def print_all(self):
        logger.info("<Header>")
        for x in self.get_header()._fields:
            logger.info(f'\t-{x}: {getattr(self.get_header(), x)}')
        logger.info("<Body>")
        for x in self.get_body()._fields:
            logger.info(f'\t-{x}: {getattr(self.get_body(), x)}')

    def print_error(self):
        return f"{self.get_error_code()}:{self.get_error_message()}"
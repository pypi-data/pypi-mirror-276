import requests
from requests.adapters import HTTPAdapter, Retry

from pyRealtor.geo import GeoLocationService
from pyRealtor.report import ReportingService
from pyRealtor.proxy import Proxy

class RealtorComService:

    def __init__(self, report_obj: ReportingService):
        self.search_api_endpoint = ""
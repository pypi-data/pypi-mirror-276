from typing import List

from dataclasses import dataclass

from .base import CtapiBaseClient


@dataclass
class Dimension:
    name: str
    value: List[str]



@dataclass
class QueryHistoryMetricParam:
    region_id: str
    service: str
    dimension: str
    item_name_list: List[str]
    start_time: int
    end_time: int
    dimensions: List[Dimension]
    fun: str
    period: int



class MonitorApi(CtapiBaseClient):

    def query_history_metric(self, param: QueryHistoryMetricParam, timeout=1):
        params = {
            "regionID": param.region_id,
            "itemNameList": param.item_name_list,
            "startTime": param.start_time,
            "endTime": param.end_time,
            "fun": param.fun,
            "service": param.service,
            "dimension": param.dimension,
            "dimensions": param.dimensions,
            "period": param.period
        }
        return self.perform_request('/v4.2/monitor/query-history-metric-data', params, 'POST', timeout=timeout)




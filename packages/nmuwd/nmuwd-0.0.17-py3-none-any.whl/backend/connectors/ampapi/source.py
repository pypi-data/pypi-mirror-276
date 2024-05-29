# ===============================================================================
# Copyright 2024 Jake Ross
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ===============================================================================
import os

import httpx

from backend.connectors.ampapi.transformer import (
    AMPAPISiteTransformer,
    AMPAPIWaterLevelTransformer,
    AMPAPIAnalyteTransformer,
)
from backend.connectors.mappings import AMPAPI_ANALYTE_MAPPING
from backend.constants import (
    TDS,
    FEET,
    URANIUM,
    SULFATE,
    ARSENIC,
    CHLORIDE,
    FLUORIDE,
    DTW,
    DTW_UNITS,
    DT_MEASURED,
    PARAMETER,
    PARAMETER_UNITS,
    PARAMETER_VALUE,
)
from backend.source import (
    BaseWaterLevelSource,
    BaseSiteSource,
    BaseAnalyteSource,
    get_most_recent,
    get_analyte_search_param,
)


def _make_url(endpoint):
    if bool(os.getenv("DEBUG")):
        return f"http://localhost:8000/{endpoint}"
    return f"https://waterdata.nmt.edu/{endpoint}"


class AMPAPISiteSource(BaseSiteSource):
    transformer_klass = AMPAPISiteTransformer

    def get_records(self):
        config = self.config
        params = {}
        if config.has_bounds():
            params["wkt"] = config.bounding_wkt()

        if config.site_limit:
            params["limit"] = config.site_limit

        if config.analyte:
            params["has_analyte"] = get_analyte_search_param(
                config.analyte, AMPAPI_ANALYTE_MAPPING
            )
        else:
            params["has_waterlevels"] = True

        return self._execute_json_request(
            _make_url("locations"), params, tag="features", timeout=30
        )


class AMPAPIAnalyteSource(BaseAnalyteSource):
    transformer_klass = AMPAPIAnalyteTransformer

    def get_records(self, parent_record):
        analyte = get_analyte_search_param(self.config.analyte, AMPAPI_ANALYTE_MAPPING)
        return self._execute_json_request(
            _make_url("waterchemistry/major"),
            params={"pointid": parent_record.id, "analyte": analyte},
            tag="",
        )

    def _extract_parameter_units(self, records):
        return [r["Units"] for r in records]

    def _extract_most_recent(self, records):
        record = get_most_recent(records, "info.CollectionDate")
        return {
            "value": record["SampleValue"],
            "datetime": record["info"]["CollectionDate"],
            "units": record["Units"],
        }

    def _extract_parameter_results(self, records):
        return [r["SampleValue"] for r in records]

    def _extract_parameter_record(self, record):
        record[PARAMETER] = self.config.analyte
        record[PARAMETER_VALUE] = record["SampleValue"]
        record[PARAMETER_UNITS] = record["Units"]
        record[DT_MEASURED] = record["info"]["CollectionDate"]
        return record


class AMPAPIWaterLevelSource(BaseWaterLevelSource):
    transformer_klass = AMPAPIWaterLevelTransformer

    def _clean_records(self, records):
        return [r for r in records if r["DepthToWaterBGS"] is not None]

    def _extract_parameter_record(self, record, *args, **kw):
        record[DTW] = record["DepthToWaterBGS"]
        record[DT_MEASURED] = (record["DateMeasured"], record["TimeMeasured"])
        record[DTW_UNITS] = FEET
        return record

    def _extract_most_recent(self, records):
        record = get_most_recent(records, "DateMeasured")
        return {
            "value": record["DepthToWaterBGS"],
            "datetime": (record["DateMeasured"], record["TimeMeasured"]),
            "units": FEET,
        }

    def _extract_parameter_results(self, records):
        return [r["DepthToWaterBGS"] for r in records]

    def get_records(self, parent_record):
        # if self.config.latest_water_level_only:
        #     params = {"pointids": parent_record.id}
        #     url = _make_url("waterlevels/latest")
        # else:
        params = {"pointid": parent_record.id}
        # just use manual waterlevels temporarily
        url = _make_url("waterlevels/manual")

        return self._execute_json_request(url, params)


# ============= EOF =============================================

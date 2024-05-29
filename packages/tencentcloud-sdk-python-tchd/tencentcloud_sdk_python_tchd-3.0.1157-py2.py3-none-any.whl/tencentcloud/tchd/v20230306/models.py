# -*- coding: utf8 -*-
# Copyright (c) 2017-2021 THL A29 Limited, a Tencent company. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import warnings

from tencentcloud.common.abstract_model import AbstractModel


class DescribeEventsRequest(AbstractModel):
    """DescribeEvents请求参数结构体

    """

    def __init__(self):
        r"""
        :param _EventDate: 事件的发生日期
        :type EventDate: str
        :param _ProductIds: 1. 不指定产品列表时将查询所有产品。
2. 产品ID示例：cvm、lb、cdb、cdn、crs
        :type ProductIds: list of str
        :param _RegionIds: 1. 不指定地域列表时将查询所有地域。
2. 查询非区域性产品事件时，地域ID指定为：non-regional
3. 其他地域ID取值请参考：https://cloud.tencent.com/document/api/213/15692
        :type RegionIds: list of str
        """
        self._EventDate = None
        self._ProductIds = None
        self._RegionIds = None

    @property
    def EventDate(self):
        return self._EventDate

    @EventDate.setter
    def EventDate(self, EventDate):
        self._EventDate = EventDate

    @property
    def ProductIds(self):
        return self._ProductIds

    @ProductIds.setter
    def ProductIds(self, ProductIds):
        self._ProductIds = ProductIds

    @property
    def RegionIds(self):
        return self._RegionIds

    @RegionIds.setter
    def RegionIds(self, RegionIds):
        self._RegionIds = RegionIds


    def _deserialize(self, params):
        self._EventDate = params.get("EventDate")
        self._ProductIds = params.get("ProductIds")
        self._RegionIds = params.get("RegionIds")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class DescribeEventsResponse(AbstractModel):
    """DescribeEvents返回参数结构体

    """

    def __init__(self):
        r"""
        :param _Data: 事件详情列表
        :type Data: :class:`tencentcloud.tchd.v20230306.models.ProductEventList`
        :param _RequestId: 唯一请求 ID，由服务端生成，每次请求都会返回（若请求因其他原因未能抵达服务端，则该次请求不会获得 RequestId）。定位问题时需要提供该次请求的 RequestId。
        :type RequestId: str
        """
        self._Data = None
        self._RequestId = None

    @property
    def Data(self):
        return self._Data

    @Data.setter
    def Data(self, Data):
        self._Data = Data

    @property
    def RequestId(self):
        return self._RequestId

    @RequestId.setter
    def RequestId(self, RequestId):
        self._RequestId = RequestId


    def _deserialize(self, params):
        if params.get("Data") is not None:
            self._Data = ProductEventList()
            self._Data._deserialize(params.get("Data"))
        self._RequestId = params.get("RequestId")


class EventDetail(AbstractModel):
    """事件详情信息，包含：产品名称、地域名称、事件开始时间、事件结束时间、事件当前状态；

    """

    def __init__(self):
        r"""
        :param _ProductId: 产品ID
        :type ProductId: str
        :param _ProductName: 产品名称
        :type ProductName: str
        :param _RegionId: 地域ID，非区域性地域返回non-regional
        :type RegionId: str
        :param _RegionName: 地域名称
        :type RegionName: str
        :param _StartTime: 事件开始时间
        :type StartTime: str
        :param _EndTime: 事件结束时间，当事件正在发生还未结束时，结束时间返回空
        :type EndTime: str
        :param _CurrentStatus: 事件当前状态：提示、异常、正常
        :type CurrentStatus: str
        """
        self._ProductId = None
        self._ProductName = None
        self._RegionId = None
        self._RegionName = None
        self._StartTime = None
        self._EndTime = None
        self._CurrentStatus = None

    @property
    def ProductId(self):
        return self._ProductId

    @ProductId.setter
    def ProductId(self, ProductId):
        self._ProductId = ProductId

    @property
    def ProductName(self):
        return self._ProductName

    @ProductName.setter
    def ProductName(self, ProductName):
        self._ProductName = ProductName

    @property
    def RegionId(self):
        return self._RegionId

    @RegionId.setter
    def RegionId(self, RegionId):
        self._RegionId = RegionId

    @property
    def RegionName(self):
        return self._RegionName

    @RegionName.setter
    def RegionName(self, RegionName):
        self._RegionName = RegionName

    @property
    def StartTime(self):
        return self._StartTime

    @StartTime.setter
    def StartTime(self, StartTime):
        self._StartTime = StartTime

    @property
    def EndTime(self):
        return self._EndTime

    @EndTime.setter
    def EndTime(self, EndTime):
        self._EndTime = EndTime

    @property
    def CurrentStatus(self):
        return self._CurrentStatus

    @CurrentStatus.setter
    def CurrentStatus(self, CurrentStatus):
        self._CurrentStatus = CurrentStatus


    def _deserialize(self, params):
        self._ProductId = params.get("ProductId")
        self._ProductName = params.get("ProductName")
        self._RegionId = params.get("RegionId")
        self._RegionName = params.get("RegionName")
        self._StartTime = params.get("StartTime")
        self._EndTime = params.get("EndTime")
        self._CurrentStatus = params.get("CurrentStatus")
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        


class ProductEventList(AbstractModel):
    """产品可用性事件详情列表

    """

    def __init__(self):
        r"""
        :param _EventList: 事件详情列表
注意：此字段可能返回 null，表示取不到有效值。
        :type EventList: list of EventDetail
        """
        self._EventList = None

    @property
    def EventList(self):
        return self._EventList

    @EventList.setter
    def EventList(self, EventList):
        self._EventList = EventList


    def _deserialize(self, params):
        if params.get("EventList") is not None:
            self._EventList = []
            for item in params.get("EventList"):
                obj = EventDetail()
                obj._deserialize(item)
                self._EventList.append(obj)
        memeber_set = set(params.keys())
        for name, value in vars(self).items():
            property_name = name[1:]
            if property_name in memeber_set:
                memeber_set.remove(property_name)
        if len(memeber_set) > 0:
            warnings.warn("%s fileds are useless." % ",".join(memeber_set))
        
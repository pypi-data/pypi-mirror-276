from __future__ import annotations

from palimpzest.datamanager import DataDirectory
from palimpzest.elements import AggregateFunction, File, Filter, Number, Schema, UserFunction, GroupBySig
from palimpzest.operators import (
    ApplyAggregateFunction,
    ApplyUserFunction,
    BaseScan,
    CacheScan,
    ConvertScan,
    FilteredScan,
    LimitScan,
    LogicalOperator,
    GroupByAggregate
)
from palimpzest.datasources import DataSource, DirectorySource, FileSource, MemorySource

from typing import List, Union

import hashlib
import json


#####################################################
#
#####################################################
class Set:
    """
    A Set is the logical abstraction for a set of DataRecords matching some Schema. It is
    also a node in the computation graph of a Dataset.

    Each Dataset consists of one or more Sets. The "initial" Set in a Dataset can be thought
    of as the Set that results from reading each DataRecord unaltered from the source. For each
    filter or transformation that is applied to the Dataset, a new Set is created which defines
    the set of DataRecords that result from applying that filter or transformation. In brief,
    the Sets define a Dataset's computation graph. Sets can also be cached to maximize the reuse
    of past computation.

    Sets are initialized with a dataset_id, a schema, and a source. The source is either an
    existing Set or a raw data source (such as a directory or S3 prefix). Sets may be initialized
    with a Filter (which defines the filtering performed on the source to obtain *this* Set),
    and a description of what this Set is meant to represent.
    """
    SET_VERSION = 0.1

    def __init__(self, 
                 schema: Schema, 
                 source: Union[Set, DataSource], 
                 desc: str=None, 
                 filter: Filter=None, 
                 aggFunc: AggregateFunction=None, 
                 groupBy: GroupBySig = None,
                 limit: int=None, 
                 fnid: str=None, 
                 cardinality: str=None,
                 image_conversion: bool=None,
                 depends_on: List[str]=None,
                 num_samples: int=None,
                 scan_start_idx: int=0,
                 nocache: bool=False):
        self._schema = schema
        self._source = source
        self._desc = desc
        self._filter = filter
        self._aggFunc = aggFunc
        self._groupBy = groupBy
        self._limit = limit
        self._fnid = fnid
        self._cardinality = cardinality
        self._image_conversion = image_conversion
        self._depends_on = depends_on
        self._num_samples = num_samples
        self._scan_start_idx = scan_start_idx
        self._nocache = nocache

    def __str__(self):
        return f"{self.__class__.__name__}(schema={self._schema}, desc={self._desc}, filter={str(self._filter)}, aggFunc={str(self._aggFunc)}, limit={str(self._limit)}, uid={self.universalIdentifier()})"

    def serialize(self):
        d = {"version": Set.SET_VERSION,
             "schema": self._schema.jsonSchema(),
             "source": self._source.serialize(),
             "desc": repr(self._desc),
             "filter": None if self._filter is None else self._filter.serialize(),
             "aggFunc": None if self._aggFunc is None else self._aggFunc.serialize(),
             "fnid": self._fnid,
             "cardinality": self._cardinality,
             "image_conversion": self._image_conversion,
             "depends_on": self._depends_on,
             "num_samples": self._num_samples,
             "scan_start_idx": self._scan_start_idx,
             "limit": self._limit,
             "groupBy": None if self._groupBy is None else GroupBySig.serialize(self._groupBy)}

        return d

    def deserialize(inputObj):
        if inputObj["version"] != Set.SET_VERSION:
            raise Exception("Cannot deserialize Set because it is the wrong version")

        # TODO: I don't believe this would actually work for the DataSources,
        #       as inputObj["schema"] is a dict. not a Schema; also need to add
        #       dataset_id to constructor here somehow
        # deserialize source depending on whether it's a Set or DataSource
        source = None
        if "version" in inputObj["source"]:
            source = Set.deserialize(inputObj["source"])

        elif inputObj["source_type"] == "directory":
            source = DirectorySource(inputObj["schema"])

        elif inputObj["source_type"] == "file":
            source = FileSource(inputObj["schema"])

        elif inputObj["source_type"] == "jsonstream":
            raise Exception("This can't possibly work, can it?")
            #source = JSONStreamSource(inputObj["schema"])

        # deserialize agg. function
        aggFuncStr = inputObj.get("aggFunc", None)
        aggFunc = None if aggFuncStr is None else AggregateFunction.deserialize(aggFuncStr)

        # deserialize agg. function
        groupByStr = inputObj.get("groupBy", None)
        groupBy = None if groupByStr is None else GroupBySig.deserialize(groupByStr)

        # deserialize limit
        limitStr = inputObj.get("limit", None)
        limit = None if limitStr is None else int(limitStr)

        fnid = inputObj.get("fnid", None)
        cardinality = inputObj.get("cardinality", None)
        image_conversion = inputObj.get("image_conversion", None)
        depends_on = inputObj.get("depends_on", None)
        num_samples = inputObj.get("num_samples", None)
        scan_start_idx = inputObj.get("scan_start_idx", None)

        return Set(schema=inputObj["schema"].jsonSchema(), 
                   source=source, 
                   desc=inputObj["desc"], 
                   filter=Filter.deserialize(inputObj["filter"]),
                   aggFunc=aggFunc,
                   fnid=fnid,
                   cardinality=cardinality,
                   image_conversion=image_conversion,
                   depends_on=depends_on,
                   num_samples=num_samples,
                   scan_start_idx=scan_start_idx,
                   limit=limit,
                   groupBy=groupBy)

    def universalIdentifier(self):
        """Return a unique identifier for this Set."""
        d = self.serialize()
        ordered = json.dumps(d, sort_keys=True)
        result = hashlib.sha256(ordered.encode()).hexdigest()
        return result

    def schema(self):
        """The Set's schema"""
        return self._schema

    def jsonSchema(self):
        """Return the JSON schema for this Set."""
        return self._schema.jsonSchema()

    def dumpSyntacticTree(self):
        """Return the syntactic tree of this Set."""
        if isinstance(self._source, DataSource):
            return (self, None)

        return (self, self._source.dumpSyntacticTree())

    def getLogicalTree(self, *args, **kwargs) -> LogicalOperator:
        """Return the logical tree of operators on Sets."""
        # set _num_samples, _scan_start_idx, and _nocache if specified
        self._num_samples = kwargs.get('num_samples', None)
        self._scan_start_idx = kwargs.get('scan_start_idx', 0)
        self._nocache = kwargs.get('nocache', False)

        # first, check to see if this set has previously been cached
        uid = self.universalIdentifier()
        if not self._nocache and DataDirectory().hasCachedAnswer(uid):
            return CacheScan(self._schema, uid, self._num_samples, self._scan_start_idx)

        # otherwise, if this Set's source is a DataSource
        if isinstance(self._source, DataSource):
            dataset_id = self._source.universalIdentifier()
            sourceSchema = self._source.schema

            if self._schema == sourceSchema:
                return BaseScan(self._schema, dataset_id, self._num_samples, self._scan_start_idx)
            else:
                return ConvertScan(self._schema, BaseScan(sourceSchema, dataset_id, self._num_samples, self._scan_start_idx), targetCacheId=uid)

        # if the Set's source is another Set, apply the appropriate scan to the Set
        if self._filter is not None:
            return FilteredScan(self._schema, self._source.getLogicalTree(*args, **kwargs), self._filter, self._depends_on, targetCacheId=uid)
        elif self._groupBy is not None:
            return GroupByAggregate(self._schema, self._source.getLogicalTree(*args, **kwargs), self._groupBy, targetCacheId=uid)
        elif self._aggFunc is not None:
            return ApplyAggregateFunction(self._schema, self._source.getLogicalTree(*args, **kwargs), self._aggFunc, targetCacheId=uid)
        elif self._limit is not None:
            return LimitScan(self._schema, self._source.getLogicalTree(*args, **kwargs), self._limit, targetCacheId=uid)
        elif self._fnid is not None:
            return ApplyUserFunction(self._schema, self._source.getLogicalTree(*args, **kwargs), self._fnid, targetCacheId=uid)
        elif not self._schema == self._source._schema:
            return ConvertScan(self._schema, self._source.getLogicalTree(*args, **kwargs), self._cardinality, self._image_conversion, self._depends_on, targetCacheId=uid)
        else:
            return self._source.getLogicalTree(*args, **kwargs)


class Dataset(Set):
    """
    A Dataset is the intended abstraction for programmers to interact with when manipulating Sets.

    Users instantiate a Dataset by specifying a `source` that either points to a
    DataSource or an existing cached Set. Users can then perform computations on
    the Dataset in an imperative fashion by leveraging functions such as `filterByStr`,
    `convert`, `aggregate`, etc. Underneath the hood, each of these operations creates
    a new Set which is cached by the DataManager. As a result, the Sets define the
    lineage of computation on a Dataset, and this enables programmers to re-use
    previously cached computation by providing it as a `source` to some future Dataset.

    To construct a Dataset, users must provide three pieces of information. First, they must
    give the Dataset a unique name using the dataset_id. Second, they need to provide a source
    or source_id, depending on whether the Dataset takes its input from a raw source (e.g. a
    directory, an S3 prefix, etc.) or from another Dataset, respectively. Third, users must
    provide a Schema for the Dataset. This Schema will be enforced when the Dataset iterates
    over the source in its __iter__ method and constructs DataRecords.
    """
    # TODO: remove num_samples, scan_start_idx, and nocache from Dataset (and Set) constructors
    def __init__(self, source: Union[str, Set], schema: Schema=File, cardinality: str = None, desc: str=None, filter: Filter=None, groupBy: GroupBySig=None, aggFunc: AggregateFunction=None, limit: int=None, fnid: str=None, image_conversion: bool=None, depends_on: Union[str, List[str]]=None, num_samples: int=None, scan_start_idx: int=0, nocache: bool=False):
        # convert source (str) -> source (DataSource) if need be
        self.source = (
            DataDirectory().getRegisteredDataset(source)
            if isinstance(source, str)
            else source
        )
        if type(depends_on) == str:
            depends_on = [depends_on]

        super().__init__(schema, self.source, cardinality=cardinality, desc=desc, filter=filter, aggFunc=aggFunc, groupBy=groupBy, limit=limit, fnid=fnid, image_conversion=image_conversion, depends_on=depends_on, num_samples=num_samples, scan_start_idx=scan_start_idx, nocache=nocache)

    def deserialize(inputObj):
        # TODO: this deserialize operation will not work; I need to finish the deserialize impl. for Schema
        if inputObj["version"] != Set.SET_VERSION:
            raise Exception("Cannot deserialize Set because it is the wrong version")

        # deserialize source depending on whether it's a Set or DataSource
        source = None
        if "version" in inputObj["source"]:
            source = Set.deserialize(inputObj["source"])

        elif inputObj["source_type"] == "directory":
            source = DirectorySource(inputObj["schema"])

        elif inputObj["source_type"] == "file":
            source = FileSource(inputObj["schema"])

        return Dataset(source, inputObj["schema"], desc=inputObj["desc"]) 

    def filter(self, f: Filter, depends_on: Union[str, List[str]]=None, desc: str="Apply filter(s)") -> Dataset:
        """
        This function creates and returns a new Set. The newly created Set uses this Set
        as its source and applies the provided filter to it.
        """
        return Dataset(source=self, schema=self.schema(), desc=desc, filter=f, depends_on=depends_on, nocache=self._nocache)

    def filterByStr(self, filterCondition: str, depends_on: Union[str, List[str]]=None, desc: str="Apply filter(s)") -> Dataset:
        """Add a filter to the Set. This filter will possibly restrict the items that are returned later."""
        f = Filter(filterCondition)

        return self.filter(f, depends_on, desc)

    def filterByFn(self, filterFn: callable, depends_on: Union[str, List[str]]=None, desc: str="Apply filter(s)") -> Dataset:
        """Add a filter to the Set. This filter will possibly restrict the items that are returned later."""
        f = Filter(filterFn=filterFn)

        return self.filter(f, depends_on, desc)

    def convert(self, newSchema: Schema, cardinality: str = None, image_conversion: bool=False, depends_on: Union[str, List[str]]=None, desc: str="Convert to new schema") -> Dataset:
        """Convert the Set to a new schema."""
        return Dataset(source=self, schema=newSchema, cardinality=cardinality, image_conversion=image_conversion, depends_on=depends_on, desc=desc, nocache=self._nocache)

    def map(self, fn: UserFunction) -> Dataset:
        """Convert the Set to a new schema."""
        if not fn.inputSchema == self.schema():
            raise Exception("Input schema of function (" + str(fn.inputSchema.getDesc()) + ") does not match schema of input Set (" + str(self.schema().getDesc()) + ")" )        
        return Dataset(source=self, schema=fn.outputSchema, fnid=fn.udfid, nocache=self._nocache)

    def aggregate(self, aggFuncDesc: str) -> Dataset:
        """Apply an aggregate function to this set"""
        return Dataset(source=self, schema=Number, desc="Aggregate results", aggFunc=AggregateFunction(aggFuncDesc), nocache=self._nocache)
    
    def groupby(self, groupBy: GroupBySig) -> Dataset:
        return Dataset(source=self, schema=groupBy.outputSchema(), desc="Group By", groupBy=groupBy, nocache=self._nocache)

    def limit(self, n: int) -> Dataset:
        """Limit the set size to no more than n rows"""
        return Dataset(source=self, schema=self.schema(), desc="LIMIT " + str(n), limit=n, nocache=self._nocache)

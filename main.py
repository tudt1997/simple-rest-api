from typing import List

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Pool(BaseModel):
    poolId: int
    poolValues: List[int]

class PercentileRequest(BaseModel):
    poolId: int
    percentile: float

class Endpoints:
    INSERT_POOL = "/insert_pool"
    CALCULATE_QUANTILE = "/calculate_quantile"

class Messages:
    POOL_DOES_NOT_EXIST = "Pool does not exist"
    CANT_INSERT_POOL_WITH_EMPTY_VALUES = "Can't insert pool with empty values"

dict_pools = {}

@app.post(Endpoints.INSERT_POOL)
def insert_pool(pool: Pool):
    # If the values are empty, then raise error
    if len(pool.poolValues) == 0:
        raise HTTPException(status_code=400, detail=Messages.CANT_INSERT_POOL_WITH_EMPTY_VALUES)

    # Insert or append values into a pool, with flag is_sorted 
    # to check if the values of the pool is sorted or not
    if pool.poolId not in dict_pools:
        dict_pools[pool.poolId] = {
            "values": pool.poolValues,
            "is_sorted": False,
        }
        status = "inserted"
    else:
        dict_pools[pool.poolId]["values"].extend(pool.poolValues)
        dict_pools[pool.poolId]["is_sorted"] = False
        status = "appended"

    return {"status": status}

@app.post(Endpoints.CALCULATE_QUANTILE)
def calculate_quantile(request: PercentileRequest):
    # If the pool doesn't exist, then raise error
    if request.poolId not in dict_pools:
        raise HTTPException(status_code=404, detail=Messages.POOL_DOES_NOT_EXIST)

    # If the pool is not sorted, then sort and reassign the flag is_sorted
    if not dict_pools[request.poolId]["is_sorted"]:
        dict_pools[request.poolId]["values"].sort()
        dict_pools[request.poolId]["is_sorted"] = True

    poolValues = dict_pools[request.poolId]["values"]

    # Calculate the integer and fractional part of a rank
    total_count = len(poolValues)
    rank = request.percentile / 100 * (total_count - 1)
    integer_part = int(rank)
    fractional_part = rank - integer_part

    # Calculate quantile based on integer and fractional part
    quantile = poolValues[integer_part]
    if fractional_part > 0:
        quantile += fractional_part * (poolValues[integer_part + 1] - poolValues[integer_part])

    return {
        "quantile": quantile,
        "totalCount": total_count,
    }

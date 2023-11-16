from pydantic import BaseModel
from typing import Type
from sqlalchemy import Result

async def sql_return_parser(sql_return: Result, output_model: Type[BaseModel]) -> Type[BaseModel]:
    row = sql_return.fetchone()
    result_out = {}

    if row:
        mid_res = row[0].__dict__.copy()
        mid_res.pop('_sa_instance_state', None)

        for field_name in output_model.model_fields.keys():
            if field_name in mid_res:
                result_out[field_name] = mid_res[field_name]
        return result_out
    else:
        return None
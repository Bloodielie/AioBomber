from typing import Dict, Optional, Union

from pydantic import BaseModel


class ServiceModel(BaseModel):
    url: str
    method: Union[str, None]
    header: Union[Dict[str, Optional[str]], None]
    static_data: Union[Dict[str, Optional[str]], None]
    dynamic_data: Dict[str, Optional[str]]

    def generator_args(self) -> Dict[str, Union[str, Dict[str, Optional[str]]]]:
        static_data = self.static_data if self.static_data is not None else {}
        header = self.header if self.header != {} else None
        return {
            "url": self.url,
            "data": {**static_data, **self.dynamic_data},
            "header": header
        }

import os
import dotenv

import json
import requests

from pathlib import Path


dotenv.load_dotenv()


class MetrikaHandler:
    def __init__(self) -> None:
        # Getting configs directory and load Metrika config
        configs_dir = Path(__file__).resolve().parent / "configs"
        with open(configs_dir / "metrika.json", "r") as f:
            config: dict = json.load(f)

        # URL of Metrika API
        self._api_url: str = config.get("metrika_api_url")

        # Request headers
        self._headers: dict = config.get("headers")

        # Add access token from environment
        self._headers["Authorization"] = "OAuth" + os.environ.get(
            "METRIKA_API_ACCESS_TOKEN", ""
        )

        # API parameters general for all data sections
        self._general_api_params: dict = config.get(
            "general_api_params"
        )

        # Add counter ID from environment
        self._general_api_params["ids"] = os.environ.get(
            "METRIKA_COUNTER_ID", 0
        )

        # API parameters specific for each data section
        # (dimensions, metrics, ...)
        self._section_specific_api_params: dict = config.get(
            "section_specific_api_params"
        )

    def __new__(cls):
        """
        Re-define __new__ method to implement Singleton pattern.
        """

        if not hasattr(cls, "instance"):
            cls.instance = super(MetrikaHandler, cls).__new__(cls)

        return cls.instance

    def get_data(self, data_section: str=None, **kwargs) -> dict:
        section_params: dict = self._section_specific_api_params.get(
            data_section, {}
        )

        response: requests.Response = requests.get(
            url=self._api_url,
            params=self._general_api_params | section_params | kwargs,
            headers=self._headers
        )

        response_json: dict = response.json()

        result = {
            "data": [],
            "errors": response_json.get("errors")
        }
        for data in response_json.get("data", []):
            result["data"].append({
                name: dim.get("name") for (name, dim) in zip(
                    section_params.get("dimensions", []),
                    data.get("dimensions")
                )
            } | {
                name: metric for (name, metric) in zip(
                    section_params.get("metrics", []),
                    data.get("metrics")
                )
            })

        return result


def main():
    print("Metrika Handler module.")


if __name__ == "__main__":
    main()

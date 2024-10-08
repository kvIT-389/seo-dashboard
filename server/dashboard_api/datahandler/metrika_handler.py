import os

import json
import requests

import datetime

from pathlib import Path


class MetrikaHandler:
    def __init__(self) -> None:
        # Getting configs directory and load Metrika config
        configs_dir = Path(__file__).resolve().parent / "configs"
        with open(configs_dir / "metrika.json", "r") as f:
            config: dict = json.load(f)

        # URL of Metrika API
        self._api_url: str = config.get("metrika_api_url")

        # Metrika API request headers
        self._headers: dict = config.get("headers")

        # Add Metrika access token from environment
        self._headers["Authorization"] = "OAuth" + os.environ.get(
            "METRIKA_API_ACCESS_TOKEN", ""
        )

        # Metrika API parameters general for all data sections
        self._general_api_params: dict = config.get(
            "general_api_params", {}
        )

        # Add Metrika counter ID from environment
        self._general_api_params["ids"] = os.environ.get(
            "METRIKA_COUNTER_ID", 0
        )

        # Metrika API parameters specific for each data section
        # (dimensions, metrics, ...)
        self._specific_api_params: dict = config.get(
            "specific_api_params", {}
        )

    def __new__(cls):
        """
        Re-define __new__ method to implement Singleton pattern.
        """

        if not hasattr(cls, "instance"):
            cls.instance = super(MetrikaHandler, cls).__new__(cls)

        return cls.instance

    def _get_dates(self, **kwargs):
        """
        Return dictionary with two dates: `date1` and `date2`
        which is `kwargs["date1"]` and `kwargs["date2"]`
        respectively or current date if one or both don't exist. 
        """

        today = datetime.date.today().isoformat()

        return dict(
            date1=kwargs.get("date1", today),
            date2=kwargs.get("date2", today)
        )

    def get_data(self, data_section: str, **kwargs):
        section_params: dict = self._specific_api_params.get(
            data_section, {}
        )

        response = requests.get(
            url=self._api_url,
            headers=self._headers,
            params=self._general_api_params |
                   section_params |
                   self._get_dates(**kwargs)
        )

        response_json: dict = response.json()

        return [
            {
                name: dim.get("name") for (name, dim) in zip(
                    section_params.get("dimensions", {}).values(),
                    data.get("dimensions")
                )
            } | {
                name: metric for (name, metric) in zip(
                    section_params.get("metrics", {}).values(),
                    data.get("metrics")
                )
            }
            for data in response_json.get("data", [])
        ]


def main():
    print("Metrika Handler module.")


if __name__ == "__main__":
    main()

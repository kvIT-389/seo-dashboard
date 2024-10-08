import os

import json
import requests

import datetime

from pathlib import Path


class TopvisorHandler:
    def __init__(self) -> None:
        # Getting configs directory and load Topvisor config
        configs_dir = Path(__file__).resolve().parent / "configs"
        with open(configs_dir / "topvisor.json", "r") as f:
            config: dict = json.load(f)

        # General URL (without specific sub-URLs) of Topvisor API
        self._general_api_url: str = config.get(
            "general_api_url", ""
        )

        # Specific sub-URLs of Topvisor API
        self._specific_api_urls: dict = config.get(
            "specific_api_urls", {}
        )

        # Topvisor API request headers
        self._headers: dict = config.get("headers", {})

        # Add Topvisor user ID from environment
        self._headers["User-Id"] = os.environ.get(
            "TOPVISOR_USER_ID", 0
        )

        # Add Topvisor API key from environment
        self._headers["Authorization"] = "bearer " + os.environ.get(
            "TOPVISOR_API_KEY", ""
        )

        # Topvisor API parameters general for all data sections
        self._general_api_params: dict = config.get(
            "general_api_params", {}
        )

        # Add Topvisor project from environment
        self._general_api_params["project_id"] = os.environ.get(
            "TOPVISOR_PROJECT_ID", 0
        )

        # Topvisor API parameters specific for each data section
        self._specific_api_params: dict = config.get(
            "specific_api_params", {}
        )

    def __new__(cls):
        """
        Re-define __new__ method to implement Singleton pattern.
        """

        if not hasattr(cls, "instance"):
            cls.instance = super(TopvisorHandler, cls).__new__(cls)

        return cls.instance

    def _get_data(self, data_section: str, **kwargs):
        section_params: dict = self._specific_api_params.get(
            data_section, {}
        )

        response = requests.get(
            url="{}/{}".format(
                self._general_api_url,
                self._specific_api_urls.get(data_section, "")
            ),
            headers=self._headers,
            json=self._general_api_params | section_params | kwargs
        )

        response_json: dict = response.json()

        return {
            "data": response_json.get("result"),
            "errors": response_json.get("errors")
        }

    def _get_dates(self, **kwargs):
        """
        Return dictionary with two dates: `date2`, which is
        `kwargs["ref_date"]` or, by default, current date,
        and `date1` which is the first day of previous month
        relatively to `date2`.
        """

        date2: datetime.date | None = kwargs.get("ref_date")
        if (date2 is None):
            date2 = datetime.date.today()
        else:
            date2 = datetime.date.fromisoformat(date2[0])

        date1 = date2.replace(day=1) - datetime.timedelta(days=1)

        return dict(
            date1=date1.isoformat(),
            date2=date2.isoformat()
        )

    def get_regions_indexes(self):
        data: dict = self._get_data("searchers_and_regions")

        regions_indexes: set[int] = set()
        for project in data.get("data", []):
            for searcher in project.get("searchers", []):
                regions_indexes |= {
                    region.get("index", 0)
                    for region in searcher.get("regions", [])
                }

        return list(regions_indexes - {0})

    def get_positions(
        self,
        regions_indexes: list[int],
        **kwargs
    ):
        data: dict = self._get_data(
            "positions", **dict(
                regions_indexes=regions_indexes
            ) | self._get_dates(**kwargs)
        ).get("data", {})

        return [
            dict(
                project_id=project.get("id"),
                search_phrase=keyword.get("name"),
                date=date,
                region_index=region.get("index"),
                position=keyword["positionsData"].get(
                    "{}:{}:{}".format(
                        date,
                        project.get("id"),
                        region.get("index")
                    ),
                    {}
                ).get("position", "--") 
            )
            for project in data["headers"]["projects"]
            for searcher in project["searchers"]
            for region in searcher["regions"]
            for keyword in data["keywords"]
            for date in data["headers"]["dates"]
        ]

    def get_tops(
        self,
        regions_indexes: list[int],
        **kwargs
    ):
        result: list[dict] = []

        for region_index in regions_indexes:
            data: dict = self._get_data(
                "tops", **dict(
                    region_index=region_index,
                    dates=list(
                        self._get_dates(**kwargs).values()
                    )
                )
            ).get("data", {})

            result.extend(
                dict(
                    date=date,
                    region_index=region_index,
                    value=tops.get("1_10")
                )
                for (date, tops) in zip(
                    data.get("dates", []),
                    data.get("tops", [])
                )
            )

        return result


def main():
    print("Topvisor Handler module.")


if __name__ == "__main__":
    main()

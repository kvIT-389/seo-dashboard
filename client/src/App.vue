<script setup>
  import axios from "axios"

  import Header from "./components/Header.vue"
  import TrafficSources from "./components/TrafficSources.vue"
  import TrafficSegmentation from "./components/TrafficSegmentation.vue"
  import Devices from "./components/Devices.vue"
  import SearchEngines from "./components/SearchEngines.vue"
  import Visits from "./components/Visits.vue"
  import GoalsConversions from "./components/GoalsConversions.vue"
  import SitePositions from "./components/SitePositions.vue"
  import SearchResultsTop from "./components/SearchResultsTop.vue"
</script>

<template>
  <Header :dashboard_name="dashboard_name"
          @update:selected-range="updateDates"></Header>

  <div class="row">
    <TrafficSources :data="sourcesData">
    </TrafficSources>

    <TrafficSegmentation :data="segmentationData">
    </TrafficSegmentation>

    <Devices :data="devicesData">
    </Devices>
  </div>
  <div class="row">
    <SearchEngines :xData="searchEnginesXData"
                   :chartData="searchEnginesChartData">
    </SearchEngines>

    <Visits :xData="visitsXData"
            :chartData="visitsChartData">
    </Visits>
  </div>
  <div class="row">
    <GoalsConversions :xData="goalConversionsXData"
                      :menuOptions="goalConversionsMenuOptions"
                      :goalAchieveData="goalAchieveData"
                      :conversionData="goalConversionData">
    </GoalsConversions>
  </div>
  <div class="row">
    <SitePositions :tableHeaders="sitePositionsTableHeaders"
                   :tableItems="sitePositionsTableItems">
    </SitePositions>

    <SearchResultsTop :beginDate="startDate"
                      :endDate="endDate"
                      :percentage="searchResultsTopPercentage">
    </SearchResultsTop>
  </div>
</template>

<script>
  const api_url = "http://localhost:8000/api/get";

  export default {
    components: {
      Header
    },
    data() {
      return {
        dashboard_name: "Байкальский Газобетон",
        startDate: null,
        startDateString: null,
        endDate: null,
        endDateString: null,
        sourcesData: [],
        segmentationData: [
          { value: 234, name: "Байкальский газобетон Иркутск" },
          { value: 735, name: "bgazobeton.ru" },
          { value: 580, name: "Газобетон иркутск" },
          { value: 484, name: "Байкальский газобетон" },
          { value: 300, name: "Газобетон" },
          {
            value: 234 + 735 + 580 + 484 + 300,
            itemStyle: {
              color: "none",
              decal: { symbol: "none" }
            },
            name:"",
            label: { show: false }
          }
        ],
        devicesData: [],
        searchEnginesXData: ["Вт", "Ср", "Чт", "Пт", "Сб", "Вс", "Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс", "Пн"],
        searchEnginesChartData: [
          {
            name: "Яндекс",
            type: "line",
            
            data: [120, 132, 101, 134, 90, 230, 210, 120, 132, 101, 134, 90, 230, 210]
          },
          {
            name: "Google",
            type: "line",
            
            data: [220, 182, 191, 234, 290, 330, 310, 220, 182, 191, 234, 290, 330, 310]
          },
          {
            name: "Bing",
            type: "line",
            
            data: [150, 232, 201, 154, 190, 330, 410, 150, 232, 201, 154, 190, 330, 410]
          },
          {
            name: "Mail.ru",
            type: "line",
            
            data: [320, 332, 301, 334, 390, 330, 320, 320, 332, 301, 334, 390, 330, 320]
          }
        ],
        visitsXData: ["Вт", "Ср", "Чт", "Пт", "Сб", "Вс", "Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс", "Пн"],
        visitsChartData: [
          {
            name: "Посетители",
            type: "line",

            data: [126, 122, 101, 13, 90, 230, 210, 120, 132, 101, 134, 90, 230, 210]
          },
          {
            name: "Новые посетители",
            type: "line",

            data: [220, 182, 191, 234, 290, 330, 310, 220, 182, 191, 234, 290, 330, 310]
          }
        ],
        goalConversionsXData: ["Вт", "Ср", "Чт", "Пт", "Сб", "Вс", "Пн"],
        goalConversionsMenuOptions: [
          { label: "Цель 1" },
          { label: "Цель 2" },
          { label: "Цель 3" },
          { label: "Цель 4" },
          { label: "Цель 5" }
        ],
        goalAchieveData: [120, 132, 101, 134, 90, 230, 210],
        goalConversionData: [2, 18, 19, 64, 29, 33, 99,],
        sitePositionsTableHeaders:[
          { text: "Запрос", value: "search_phrase", width: 600},
          { text: "Дата 1", value: "position1", width: 70},
          { text: "Дата 2", value: "position2", width: 70}
        ],
        sitePositionsTableItems: [
          { search_phrase: "газобетон", position1: "3", position2: "3"},
          { search_phrase: "газобетон в иркутске", position1: "1", position2: "1"},
          { search_phrase: "где качественный газобетон в иркутске цена за куб купить сегодня дёшево", position1: "1", position2: "2"},
          { search_phrase: "купить газобетон", position1: "1", position2: "1"},
          { search_phrase: "купить газобетон в иркутске", position1: "1", position2: "1"},
          { search_phrase: "газобетон иркутск цена", position1: "1", position2: "1"},
          { search_phrase: "купить газобетон в иркутске цены", position1: "1", position2: "1"},
          { search_phrase: "газобетон цена", position1: "1", position2: "1"},
          { search_phrase: "газобетон цена за куб", position1: "1", position2: "1"},
          { search_phrase: "стоимость газобетона в иркутске цены", position1: "1", position2: "1"},
          { search_phrase: "газобетон", position1: "3", position2: "3"},
          { search_phrase: "газобетон в иркутске", position1: "1", position2: "1"},
          { search_phrase: "где качественный газобетон в иркутске цена за куб купить сегодня дёшево", position1: "1", position2: "2"},
          { search_phrase: "купить газобетон", position1: "1", position2: "1"},
          { search_phrase: "купить газобетон в иркутске", position1: "1", position2: "1"},
          { search_phrase: "газобетон иркутск цена", position1: "1", position2: "1"},
          { search_phrase: "купить газобетон в иркутске цены", position1: "1", position2: "1"},
          { search_phrase: "газобетон цена", position1: "1", position2: "1"},
          { search_phrase: "газобетон цена за куб", position1: "1", position2: "1"},
          { search_phrase: "стоимость газобетона в иркутске цены", position1: "1", position2: "1"}
        ],
        searchResultsTopPercentage: 93
      }
    },
    mounted() {
      this.updateData();
    },
    methods: {
      updateDates(newRange) {

        this.startDate = new Date(newRange[0]);
        this.startDate.setHours(0, 0, 0, 0);

        this.endDate = new Date(newRange[1]);
        this.endDate.setHours(0, 0, 0, 0);

        const options = { day: "numeric", month: "numeric", year: "numeric" };

        this.startDateString = this.startDate.toLocaleDateString("ru-RU", options);
        this.endDateString = this.endDate.toLocaleDateString("ru-RU", options);

        this.updateData();
      },
      async getData(data_section) {
        try {
          let params = {}
          if (this.startDate) {
            params.date1 = this.startDate?.toISOString().split("T")[0];
          }
          if (this.endDate) {
            params.date2 = this.endDate?.toISOString().split("T")[0];
          }

          const response = await axios.get(
            `${api_url}/${data_section}?` + new URLSearchParams(params)
          );

          const response_json = await response.data;
          return response_json;
        }
        catch (error) {
          console.log(error);

          return {
            data: []
          };
        }
      },
      async updateData() {
        // Devices
        const devices_data = await this.getData("device_categories");
        this.devicesData = [];

        devices_data.data.map((item) => {
          this.devicesData.push({
            name: item.device_category,
            value: item.visits
          })
        });

        // Traffic Sources

        const sources_data = await this.getData("traffic_sources");
        this.sourcesData = [];
        let others_visits = 0;

        sources_data.data.map((item) => {
          if (this.sourcesData.length < 4) {
            this.sourcesData.push({
              name: item.traffic_source,
              value: item.visits
            });
          }
          else {
            others_visits += item.visits;
          }
        });

        this.sourcesData.push({
          name: "Others",
          value: others_visits
        });
      }
    }
  }
</script>

<style scoped>
  .row {
    display: flex;
    justify-content: space-between;
    margin: 1.5rem;
    margin-top: 0;
  }
  .row {
    height: 512px;
  }
  .row:last-child {
    height: auto;
  }
  .row > *:not(:last-child) {
    margin-right: 1.5rem;
  }
</style>

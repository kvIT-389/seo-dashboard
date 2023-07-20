<script setup>
  import Header from "./components/Header.vue"
  import TrafficSources from "./components/TrafficSources.vue"
  import TrafficSegmentation from "./components/TrafficSegmentation.vue"
  import Devices from "./components/Devices.vue"
  import SearchEngines from "./components/SearchEngines.vue"
  import Visits from "./components/Visits.vue"
  import GoalsConversions from "./components/GoalsConversions.vue"
  import SitePositions from "./components/SitePositions.vue"
</script>

<template>
  <Header :dashboard_name="dashboard_name"
          @update:start-date="updateBeginDate"
          @update:end-date="updateEndDate"></Header>

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
  </div>
</template>

<script>
  export default {
    components: {
      Header
    },
    data() {
      return {
        dashboard_name: "Байкальский Газобетон",
        startDate: null,
        endDate: null,
        sourcesData: [
          { value: 348, name: "Прямые заходы" },
          { value: 735, name: "Переходы из поисковых систем" },
          { value: 580, name: "Переходы по ссылкам на сайтах" },
          { value: 484, name: "Переходы из социальных сетей" },
          { value: 3, name: "Остальные" }
        ],
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
        devicesData: [
          { value: 1048, name: "Смартфоны" },
          { value: 735, name: "Персональные компьютеры" },
          { value: 580, name: "Планшеты" },
          { value: 484, name: "ТВ" }
        ],
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
        top10Percentage: 93
      }
    },
    methods: {
      updateBeginDate(new_begin_date) {
        const startDate = new Date(new_begin_date);
        const options = { day: "numeric", month: "numeric", year: "numeric" };

        this.startDate = startDate.toLocaleDateString("ru-RU", options);
      },
      updateEndDate(new_end_date) {
        const endDate = new Date(new_end_date);
        const options = { day: "numeric", month: "numeric", year: "numeric" };

        this.endDate = endDate.toLocaleDateString("ru-RU", options);
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

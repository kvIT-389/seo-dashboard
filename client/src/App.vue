<script setup>
  import Header from "./components/Header.vue"
  import TrafficSources from "./components/TrafficSources.vue"
  import TrafficSegmentation from "./components/TrafficSegmentation.vue"
</script>

<template>
  <Header :dashboard_name="dashboard_name"
          @update:start-date="updateBeginDate"
          @update:end-date="updateEndDate"></Header>

  <div class="row">
    <TrafficSources :data="sourcesData"></TrafficSources>
    <TrafficSegmentation :data="segmentationData"></TrafficSegmentation>
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
    justify-content: flex-start;
  }
  .row > * {
    flex: 1;
    margin-right: 50px;
  }
  .row > *:last-child {
  margin-right: 15px;
  }
</style>

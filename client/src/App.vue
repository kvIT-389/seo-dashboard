<script setup>
  import Header from "./components/Header.vue"
  import TrafficSources from "./components/TrafficSources.vue"
</script>

<template>
  <Header :dashboard_name="dashboard_name"
          @update:start-date="updateBeginDate"
          @update:end-date="updateEndDate"></Header>

  <TrafficSources :data="sourcesData"></TrafficSources>
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
        ]
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

<script setup>
import Header from "./components/Header.vue"
</script>

<template>
  <Header :dashboard_name="dashboard_name"
          @update:start-date="handleStartDateUpdated"
          @update:end-date="handleEndDateUpdated"></Header>
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
        endDate: null
      }
    },
    methods: {
      handleStartDateUpdated(newStartDate) {
        const startDate = new Date(newStartDate);
        const options = { day: "numeric", month: "numeric", year: "numeric" };

        this.startDate = startDate.toLocaleDateString("ru-RU", options);
        this.dateone =  this.startDate;
      },
      handleEndDateUpdated(newEndDate) {
        const endDate = new Date(newEndDate);
        const options = { day: "numeric", month: "numeric", year: "numeric" };

        this.endDate = endDate.toLocaleDateString("ru-RU", options);
        this.datetwo =  this.endDate;
      }
    }
  }
</script>

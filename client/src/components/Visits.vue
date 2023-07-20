<template>
  <div class="chart-container">
    <div ref="chartVisits" id="chartVisits"></div>
  </div>
</template>

<script setup>
  import { onMounted, ref } from "vue";
  import * as echarts from "echarts";

  const props = defineProps(["xData", "chartData"]);
  const option = ref({
    title: {
      text: "Посетители",
      left: "center",
      top: 20,
      textStyle: {
        fontSize: 24,
        fontWeight: "bold",
        fontFamily: "Panton",
        color: "#352958" 
      }
    },
    tooltip: {
      trigger: "axis"
    },
    grid: {
      left: "3%",
      right: "4%",
      bottom: "3%",
      containLabel: true
    },
    toolbox: {
      feature: {
        saveAsImage: {}
      }
    },
    xAxis: {
      type: "category",
      boundaryGap: false,
      data: props.xData
    },
    yAxis: {
      type: "value"
    },
    series: props.chartData
  });

  onMounted(() => {
    const chart = echarts.init(document.getElementById("chartVisits"));
    chart.setOption(option.value);
  });
</script>

<style scoped>
  .chart-container {
    width: 100%;
    max-width: 1000px;
  }
  #chartVisits {
    width: 100%;
    height: 100%;
    background-color: white;
    border-radius: 0.7rem;
  }
</style>

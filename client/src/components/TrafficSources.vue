<template>
  <div class="chart-container">
    <div ref="chartTrafficSources" id="chartTrafficSources"></div>
  </div>
</template>

<script setup>
  import { computed, onMounted, onUpdated } from "vue";
  import * as echarts from "echarts";

  const props = defineProps({
    data: {
      type: Array,
      default: () => []
    }
  });

  const chartOptions = computed(() => {
    let option = {
      title: {
        text: "Источники трафика",
        left: "center",
        top: 20,
        textStyle: {
          
          fontSize: 24,
          fontWeight: "bold",
          fontFamily: "Panton",
          color: "#352958" 
        }
      },
      toolbox: {
        feature: {
          saveAsImage: {}
        }
      },
      tooltip: {
        trigger: "item"
      },
      legend: {
        orient: "horizontal",
        top: "bottom",
        textStyle: {
          fontSize: 12,
          fontWeight: "bold",
          fontFamily: "Panton",
          color: "#352958" 
        }
      },
      grid: {
        containLabel: true
      },
      series: [
        {
          name: "Access From",
          type: "pie",
          radius: "50%",
          data: props.data,
          emphasis: {
            itemStyle: {
              shadowBlur: 10,
              shadowOffsetX: 0,
              shadowColor: "rgba(0, 0, 0, 0.5)"
            }
          }
        }
      ]
    };

    return option;
  });

  let chart;

  onMounted(() => {
    chart = echarts.init(document.getElementById("chartTrafficSources"));
    chart.setOption(chartOptions.value);
  });

  onUpdated(() => {
    chartOptions.value.series[0].data = props.data;
    chart.setOption(chartOptions.value);
  });
</script>

<style scoped>
  .chart-title {
    font-family: "Panton";
  }
  .chart-legend {
    font-family: "Panton";
  }
  .chart-container {
    width: 100%;
    max-width: 640px;
    margin-right: auto;
  }
  #chartTrafficSources {
    width: 100%;
    height: 100%;
    background-color: white;
    border-radius: 0.7rem;
  }
</style>

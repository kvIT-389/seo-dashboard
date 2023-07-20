<template>
  <div class="chart-container">
    <div ref="chartDevices" id="chartDevices"></div>
  </div>
</template>

<script setup>
  import { onMounted, ref } from "vue";
  import * as echarts from "echarts";

  const props = defineProps({
    data: {
      type: Array,
      default: () => []
    }
  });
  const chartOptions = ref({
    title: {
      text: "Устройства",
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
      trigger: "item"
    },
    legend: {
      bottom: "5%",
      left: "center",
      textStyle: {
          fontSize: 12,
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
    series: [
      {
        name: "Access From",
        type: "pie",
        radius: ["20%", "55%"],
        avoidLabelOverlap: false,
        label: {
          show: false,
          position: "center"
        },
        emphasis: {
          label: {
            show: true,
            fontSize: 14,
            fontWeight: "bold"
          }
        },
        labelLine: {
          show: false
        },
        data: props.data
      }
    ]
  });

  onMounted(() => {
    const chart = echarts.init(document.getElementById("chartDevices"));
    chart.setOption(chartOptions.value);
  });
</script>

<style scoped>
  .chart-container {
    width: 100%;
    max-width: 640px;
  }
  #chartDevices {
    width: 100%;
    height: 100%;
    background-color: white;
    border-radius: 0.7rem;
  }
</style>

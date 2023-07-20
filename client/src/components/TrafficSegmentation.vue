<template>
  <div class="chart-container">
    <div ref="chartSegmentation" id="chartSegmentation"></div>
    <div class="chart-legend" ref="chartLegend"></div>
  </div>
</template>

<script setup>
  import { computed, onMounted, defineProps } from "vue";
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
        text: "Сегментация трафика",
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
      toolbox: {
        feature: {
          saveAsImage: {}
        }
      },
      legend: {
        orient: "horizontal",
        bottom: 20,
        left: "center",
        selectedMode: false,
        data: props.data.map(item => item.name),
        textStyle: {
        
        fontSize: 12,
        fontWeight: "bold",
        fontFamily: "Panton",
        color: "#352958" 
        // Используем ваш шрифт для заголовка
      }
      },
      series: [
        {
          name: "Access From",
          type: "pie",
          radius: ["40%", "70%"],
          center: ["50%", "65%"],
          startAngle: 180,
          label: {
            show: true,
            formatter(param) {
              return param.name + " (" + param.percent * 2 + "%)";
            }
          },
          data: props.data
        }
      ]
    };

    return option;
  });

  onMounted(() => {
    const chart = echarts.init(document.getElementById("chartSegmentation"));
    chart.setOption(chartOptions.value);

    const legend = chart.getModel().getComponent("legend");
    legend.orient = "horizontal";
    legend.bottom = 0;
    legend.left = "center";

    chart.resize();

    chart.setOption({ legend: legend.options });
  });
</script>

<style scoped>
  .chart-container {
    width: 100%;
    max-width: 640px;
    margin-right: auto;
  }
  .chart-title {
    text-align: center;
  }
  #chartSegmentation {
    width: 100%;
    height: 100%;
    background-color: white;
    border-radius: 0.7rem;
  }
  .chart-legend {
    margin-top: 0.7rem;
  }
</style>

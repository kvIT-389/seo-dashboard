<template>
  <div class="chart-container">
    <div ref="chartConversion" id="chartConversion"></div>
  </div>
  <div class="menu-container">
    <select v-model="selectedOption" @change="handleMenuClick()" class="rounded-blue">
      <option v-for="option in options" :key="option.value">{{ option.label }}</option>
    </select>
  </div>
</template>

<script setup>
  import { onMounted, ref, defineProps, defineEmits } from "vue";
  import * as echarts from "echarts";

  const emits = defineEmits(["selectedOptionChanged"]);
  const props = defineProps({
    goalAchieveData: {
      type: Array,
      required: true
    },
    xData:{
      type: Array,
      required: true
    },
    conversionData: {
      type: Array,
      required: true
    },
    menuOptions: {
      type: Array,
      required: true
    }
  });

  const selectedOption = ref(null);
  const options = ref([...props.menuOptions]);

  const option = ref({
    title: {
      text: "Конверсии",
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
      top: "15%",
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
    yAxis: [
      {
        type: "value",
        position: "left"
      },
      {
        type: "value",
        position: "right",
        min: 0,
        max: 100,
        axisLabel: {
          formatter: "{value}%"
        }
      }
    ],
    series: [
      {
        name: "Достижение цели",
        type: "line",
        data: props.goalAchieveData,
        lineStyle: {
          // color: "blue"
        },
        itemStyle: {
          // color: "blue"
        },
        yAxisIndex: 0
      },
      {
        name: "Конверсия",
        type: "line",
        data: props.conversionData,
        lineStyle: { 
          color: "red"
        },
        itemStyle: {
          color: "red"
        },
        yAxisIndex: 1
      }
    ]
  });

  const handleMenuClick = () => {
    emits("selectedOptionChanged", selectedOption);
  };

  onMounted(() => {
    const chart = echarts.init(document.getElementById("chartConversion"));
    chart.setOption(option.value);
  });
</script>

<style scoped>
  .menu-container {
    position: absolute;
    margin: 1.2rem;
  }
  .chart-container {
    width: 100%;
    max-width: 2000px;
  }
  #chartConversion {
    width: 100%;
    height: 100%;
    background-color: white;
    border-radius: 0.7rem;
  }
  .rounded-blue {
    border-radius: 0.7rem;
    background-color: var(--lilac);
    color: #3d3d3d;
    padding: 0.5rem;
    border: none;
    box-shadow: 5px 0px 10px #e0e3ffaa,
                5px 0px 10px #ffffff;
  }
  .rounded-blue option {
    color: #3d3d3d;
    border-radius: 0.7rem;
  }
</style>

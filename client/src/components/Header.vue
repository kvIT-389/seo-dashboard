<script setup>
defineProps({
  dashboard_name: String
})
</script>

<template>
  <header>
    <h1>{{ dashboard_name }}</h1>
    <VueDatePicker v-model="selectedRange" range
      :format="dateFormat"
      locale="ru" 
      cancelText="Отменить" 
      selectText="Выбрать" 
      :clearable="false"
      :enable-time-picker="false" 
      class="custom-datepicker"
      :disabled-date="disableFutureDates">
    </VueDatePicker>
  </header>
</template>

<script>
  import { ref, watch } from 'vue';
  import VueDatePicker from '@vuepic/vue-datepicker';
  import '@vuepic/vue-datepicker/dist/main.css';

  export default {
    name: 'MyComponent',
    components: {
      VueDatePicker
    },
    data() {
      const startDate = ref(null);
      const endDate = ref(null);
      const selectedRange = ref([]);
      const dateFormat = 'dd.MM.yyyy';

      watch(selectedRange, (newRange) => {
        startDate.value = newRange[0];
        endDate.value = newRange[1];

        this.$emit("update:selected-range", newRange)
      });

      return {
        startDate,
        endDate,
        selectedRange,
        dateFormat
      };
    },
    methods: {
      disableFutureDates(date) {
        const today = new Date();
        today.setHours(0, 0, 0, 0);

        return date > today;
      }
    },
    watch: {
      startDate(newStartDate) {
        this.$emit('update:start-date', newStartDate);
      },
      endDate(newEndDate) {
        this.$emit('update:end-date', newEndDate);
      }
    }
  };
</script>

<style scoped>
  header {
    display: flex;
    align-items: center;
    flex-wrap: wrap;
    margin: 1.5rem;
    padding: 1rem;
    border-radius: 0.7rem;
    background-color: white;
  }
  h1 {
    display: inline;
    margin: 0;
    margin-right: auto;
    font-size: 2.4rem;
    vertical-align: middle;
  }
  .custom-datepicker {
    display: flex;
    align-items: center;
    flex-basis: auto;
    width: auto;
    font-size: 1.25rem;
    color: #352958;
  }
</style>

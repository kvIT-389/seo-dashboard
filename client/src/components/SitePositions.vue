<template>
  <div class="tableContainer">
    <EasyDataTable
      :headers="headers"
      :items="items"
      buttons-pagination
      :rows-per-page="5"
      :hide-rows-per-page="true"
      theme-color="#f23b67"
      border-cell
      class="customize-table"
    />
  </div>
</template>

<script setup>
  import { defineProps } from "vue";
  import EasyDataTable from "vue3-easy-data-table";
  import "vue3-easy-data-table/dist/style.css";

  const props = defineProps({
    tableHeaders: {
      type: Array,
      default: () => []
    },
    tableItems: {
      type: Array,
      default: () => []
    }
  });

  const headers = props.tableHeaders;
  const items = props.tableItems;
</script>

<style>
  .tableContainer {
    display: flex;
    width: 60%;
    max-width: 1442px;
    padding: 1.2rem;
    border-radius: 0.7rem;
    background-color: white;
  }
  .customize-table {
    --easy-table-header-background-color: white;
    --easy-table-body-row-background-color: white;
    --easy-table-footer-background-color: white;
    --easy-table-border-radius: 50px;
    width: 100%;
    font-family: "Panton";
  }
</style>

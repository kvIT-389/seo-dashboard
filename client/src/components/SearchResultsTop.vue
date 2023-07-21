<template>
  <div class="topContainer">
      <h2>Процент вывода в топ-10</h2>
      <p class="date">{{ beginDate }} - {{ endDate }}</p>
      <p class="percentage">{{ percentage }}%</p>
  </div>
</template>

<script>
  export default {
    props: {
      beginDate: {
        type: String,
        required: true
      },
      endDate: {
        type: String,
        required: true
      },
      percentage: {
        type: Number,
        required: true
      }
    }
  }
</script>

<style>
  h2 {
      color: #352958;
      text-align: center;
      font-size: 2rem;
      font-style: normal;
      font-weight: 600;
      line-height: 115%;
      font-family: "Panton";
  }
  .topContainer {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      max-width: 500px;
      width: 25%;
      padding: 0.9rem;
      background-color: white;
      border-radius: 0.7rem;
      font-family: "Panton";
  }
  .date {
      color: #352958;
      text-align: center;
      font-family: Panton;
      font-size: 25px;
      font-style: normal;
      font-weight: 600;
      line-height: 115%;
      margin-top: 0.2rem;
      margin-bottom: 0.25rem;
  }
  .percentage {
     font-family: "Panton";
      color: #f23b67;
      text-align: center;
      font-size: 60px;
      font-style: normal;
      font-weight: 600;
      line-height: normal;   
      margin-top: 0.1rem;
      margin-bottom: 1rem;
  }
</style>

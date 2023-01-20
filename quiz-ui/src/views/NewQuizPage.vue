<template>
  <body>
    <div class="newQuiz">
      <div class="d-flex flex-column gap-2">
        <h2>Enter your name :</h2>
        <br>
        <input type="text" placeholder="Username" v-model="username">
        <button @click="launchNewQuiz"> Start !</button>
    </div>
    </div>
  </body>
</template>

<script>
import participationStorageService from "@/services/ParticipationStorageService";
export default {
  name: "NewQuiz",
  data() {
    return {
      username: ''
    }
  },
  methods: {
    launchNewQuiz() {
      participationStorageService.savePlayerName(this.username);
      console.log("Launch new quiz with", this.username);
      this.$router.push('/quiz');
    }
  }
}

</script>

<style>

.newQuiz {
  max-width: 1000px;
  margin: 0 auto;
  text-align: center;
}

</style>

<template>

  <body>
    <div class="d-flex flex-column">
      
      <div class="container">
        <h1>Your favorite quiz results !</h1>
        <h2>Leaderboard :</h2>

        <div v-for="(player, index) in scores" :class="{ active: player.isActive }" v-bind:id="index">
          <div>
            {{ player.playerName }} - {{ player.score }}
          </div>
        </div>


        <br>
        <div class="bt">
          <button @click="goNewQuiz"> 
            Go to quiz
          </button>
        </div>
      </div>
    </div>
  </body>
</template>

<script>

import quizApiService from "@/services/QuizApiService";

export default {
  name: "HomePage",
  data() {
    return {
      size: 1,
      registeredScores: [],
      scores: []
    };
  },
  async created() {
    console.log("Composant Home page 'created'")
    var json = await quizApiService.getQuizInfo()
    this.scores = json.data.scores
    this.size =json.data.size

  },
  methods: {
    goNewQuiz() {
      this.$router.push('/newquiz');
    }
  }
};
</script>


<style>
.container {
  max-width: 1000px;
  margin: 0 auto;
  text-align: center;
  font-size: larger;
}

.mainblock {
  font-size: 1em;
}

.bt {
  cursor: pointer;
}
</style>

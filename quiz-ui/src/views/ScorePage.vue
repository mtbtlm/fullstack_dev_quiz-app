<template>
  <body>
    <div class="score">
      <h1>{{ playerName }}, your score is: {{ playerScore }} </h1>
      <p> You are ranked {{ classement }} ! </p>
      <h2>Leaderboard :</h2>

      <div v-for="(player, index) in scores" :class="{ active: player.isActive }" v-bind:id="index">
          <div>
            {{ player.playerName }} - {{ player.score }}
          </div>
        </div>
        <br>
        <button @click="goHome">Home Page</button>

    </div> 




  </body>
</template>

<script>
import participationStorageService from "@/services/ParticipationStorageService";
import quizApiService from "@/services/QuizApiService";
export default {
  name: "ScorePage",
  data() {
    return {
      scores: [],
      playerScore: 0,
      playerName: '',
      classement: '',
      playerNames: [],
      registeredScores: []
    }
  },
  async created() {
    console.log("Composant Score 'created'")
    this.playerName = participationStorageService.getPlayerName()
    this.playerScore = participationStorageService.getParticipationScore()
    var json = await quizApiService.getQuizInfo()
    this.scores = json.data.scores


    var rank = 1
    console.log(this.registeredScores)
    for (var player of this.scores) {

      if (player.score == this.playerScore) {
        break;
      }
      rank++
    }
    this.classement = rank
    this.classement += (rank === 1) ? "st" : "th"
  },
  methods: {
    goHome() {
      this.$router.push('/');
    }
  }
}

</script>
<style>
.score {
  max-width: 800px;
  margin: 0 auto;
  text-align: center;
}

h1 {
  font-size: 2em;
  margin-bottom: 0.5em;
}

h2 {
  font-size: 1.5em;
  margin-top: 0;
  margin-bottom: 0.5em;
}
</style>

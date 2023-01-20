<template>

  <body>
    <div class="adminSect">
      <div class="d-flex flex-column gap-3">
      <h1>Administrator Section</h1>
      <div v-if="token != ''">
        <p>Choose an option :</p>
        <div class="d-flex flex-column gap-3">
          <button @click="gotoShowQuestionsPage"> Show all questions </button><br />
          <button @click="gotoPostQuestionPage">Add question</button><br />
          <button @click="rebuildDB"> Rebuild DB </button><br />
          <div v-if="db_rebuilt == true">
            Database Rebuilt!
          </div>
          
          
        </div>
      </div>
      <div v-else>
        <p>You must login first!</p>
        <button @click="gotoLoginPage"> Go to login page </button><br/>
      </div>
    </div>


    </div>
    
  </body>
</template>

<script>
import adminStorageService from "@/services/AdminStorage";
import quizApiService from "@/services/QuizApiService";
export default {
  name: "AdminTools",
  data() {
    return {
      token: adminStorageService.getToken(),
      db_rebuilt: false
    }
  },
  methods: {
    gotoLoginPage() {
      this.$router.push('/login');
    },
    gotoPostQuestionPage() {
      this.$router.push('/postquestion');
    },
    gotoShowQuestionsPage() {
      this.$router.push('/showquestions');
    },
    async rebuildDB() {
      if(confirm("If the database is empty, confirm to rebuild the database")){
        await quizApiService.rebuildDB(this.token)
        this.db_rebuilt = true;
      }
    },
  }
}

</script>

<style>

.adminSect {
  max-width: 1000px;
  margin: 0 auto;
  text-align: center;
}


</style>

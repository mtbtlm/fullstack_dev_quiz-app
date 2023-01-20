<template>

  <div style="text-align: center">
    <button @click.prevent="goBack">Back</button><br><br>
    <button @click.prevent="deleteAll">Delete all Questions</button><br><br><br>

  </div>
  
  <h3 v-if="all_questions.length==0" style="text-align: center;">No questions in the database yet!</h3>
  <table v-else style="text-align: center">
    <tr>
      <label>
        <h2><b>List of {{ totalNumberOfQuestion }} questions:</b></h2>
        <br><br><br>
      </label>
    </tr>
    <tr>
      <div class="answer" v-for="(question, index) in all_questions" :class="{ active: question.isActive }" v-bind:id="index">

        <label>
          Question {{ index+1 }}:<br />
          <span class="question-title" :title="question.title">{{ question.title }}</span>
          <br>
          <img v-if="question.image" :src="question.image" class="question-image" alt="Question image" />
          <br />


          <br><button @click.prevent="showDetails(question.position)">Details</button>
          <br /><br />
        </label>
      </div>
    </tr>
  </table>
</template>

<script>
import quizApiService from "@/services/QuizApiService";
import adminStorageService from "@/services/AdminStorage";
export default {
  name: "showquestions",
  data() {
    return {
      all_questions: [],
      totalNumberOfQuestion: 0
    };
  },
  async created() {
    console.log("Composant ShowQuestionsPage 'created'")
    this.loadQuestions()
  },
  methods: {
    addAnswer() {
      this.answers.push(new Answer());
    },
    goBack() {
      this.$router.push('/admintools');
    },
    async deleteAll() {
      if (confirm("Confirm want to delete ALL questions, you might have to reload page after!")) {
        var token = await adminStorageService.getToken();
        var response = await quizApiService.deleteAllQuestion(token);
        console.log("Deleted All Questions.\nResponse:\n" + JSON.stringify(response));
        this.loadQuestions()
      }
    },
    showDetails(position) {
      adminStorageService.setQuestionToDetail(position)
      this.$router.push('/editor');
    },
    async loadQuestions() {
      var json = await quizApiService.getQuizInfo()
      json = await quizApiService.getAllQuestions()
      this.all_questions = json.data.questions
      this.totalNumberOfQuestion = this.all_questions.length
      console.log(this.all_questions)
      console.log(this.all_questions["0"])
    }
  },
};

export class Question {
  text = "";
  title = "";
  image = "";
  position = "";
  possibleAnswers = "";

  constructor() {
    this.text = "";
    this.title = "";
    this.image = "";
    this.position = 1;
    this.possibleAnswers = "";
  }

}

export class Answer {
  text = "";
  isCorrect = "";

  constructor() {
    this.text = "";
    this.isCorrect = false;
  }

}
</script>

<style>
.answer:not(:first-child) {
  margin-top: 1rem;
}

.question-image {
  width: 350px;
  height: 200px;
  margin-top: 1rem;
  object-fit: cover;
}

.question-title {
  font-size: 1.2rem;
  font-weight: bold;
}

</style>

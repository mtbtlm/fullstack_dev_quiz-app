<template>
  <div class="questionEditor">
    <table style="text-align: center">
      <h1>Question {{question.questionPosition}}:</h1>
      <br>
      <p class="question-title"> {{question.questionTitle}} </p>
      <p class="question-title"> {{question.questionText}} </p>
      <img v-if="question.questionImage" :src="question.questionImage" class="question-image" />
      <br>
      <h1>Answers: </h1><br>
      <div v-for="answer in question.possibleAnswers">
        <p>{{ answer.text }}</p>
      </div>
      <br>
      <br>
      <div class="d-flex flex-column gap-3">
        <button @click.prevent="gotoUpdatePage">Go to update this question</button><br>
        <button @click.prevent="deleteQuestion">Delete this question</button><br>
        <button @click.prevent="goBack">Back</button><br>
      </div>
    </table>

  </div>

  
</template>

<script>
import quizApiService from "@/services/QuizApiService";
import adminStorageService from "@/services/AdminStorage";
export default {
  name:"QuestionEditor",
  data() {
        return {
            question: {
                questionTitle: '',
                questionText: '',
                questionImage: '',
                possibleAnswers: [],
                questionPosition: 1,
                questionId: 1
            }
        }
  },
  async created() {
    console.log("Composant QuestionEditor 'created'")
    var position = adminStorageService.getQuestionToDetail()
    this.loadQuestionByPosition(position)
  },
  methods: {
    async loadQuestionByPosition(position) {
        var json = await quizApiService.getQuestion(position)
        this.question.questionPosition = position
        this.question.questionTitle = json.data.questionTitle
        this.question.questionText = json.data.text
        this.question.questionImage = json.data.image
        this.question.possibleAnswers = json.data.possibleAnswers
        // this.question.questionId = json.data.id
    },
    gotoUpdatePage() {
      this.$router.push('/modifyquestion');
    },
    goBack() {
      this.$router.push('/showquestions');
    },
    async deleteQuestion() {
      if (confirm("Are you sure?")) {
        var token = await adminStorageService.getToken();
        var id_position = await quizApiService.idByPosition(this.question.questionPosition);
        var q_id = id_position.data.id_question
        console.log(q_id)

        var response = await quizApiService.deleteQuestion(token, q_id);
        console.log("Deleted question at position " + this.question.questionPosition + "\nWith ID = " + q_id + "\nResponse:\n" + JSON.stringify(response));

        this.$router.push('/showquestions');
      }
    }
  }
};
</script>

<style>
.answer:not(:first-child) {
  margin-top: 1rem;
}

.question-image {
  width: 300px;
  height: 300px;
  object-fit: cover;
  border-radius: 10%;
}

.question-title {
  font-size: 1.2rem;
  font-weight: bold;
}

.questionEditor {
  max-width: 1000px;
  margin: 0 auto;
  text-align: center;
}

</style>
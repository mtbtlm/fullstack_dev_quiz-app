<template>
    <div class="questionManager">
        <table >
            <tr><h1>Question {{ currentQuestionPosition }} / {{ totalNumberOfQuestion }}</h1></tr>
            <tr><QuestionDisplay :question="currentQuestion" @answerSelected="answerClickedHandler" /></tr>
            <br>
        </table>
    </div>
</template>

<script>
import participationStorageService from "@/services/ParticipationStorageService";
import quizApiService from "@/services/QuizApiService";
import QuestionDisplay from "@/views/QuestionDisplay.vue";
export default {
    name: "QuestionManager",
    data() {
        return {
            currentQuestion: {
                questionTitle: '',
                questionText: '',
                questionImage: '',
                possibleAnswers: [],
            },
            currentQuestionPosition: 1,
            totalNumberOfQuestion: 0,
            score: 1,
            answers: [],
        }
    },
    async created() {
        console.log("Composant QuestionManager 'created'")
        console.log(this.currentQuestionPosition)
        this.loadQuestionByPosition(this.currentQuestionPosition)

        var json = await quizApiService.getQuizInfo()
        this.totalNumberOfQuestion = json.data.size
    },
    components: {
        QuestionDisplay
    },
    methods: {
        async loadQuestions() {
            var json = await quizApiService.getQuizInfo()
            json = await quizApiService.getAllQuestions()
            this.all_questions = json.data.questions
            this.totalNumberOfQuestion = this.all_questions.length
            console.log(this.all_questions)
            console.log(this.all_questions["0"])
        },
        async loadQuestionByPosition(position) {
            var json = await quizApiService.getQuestion(position)
            this.currentQuestion.questionTitle = json.data.questionTitle
            this.currentQuestion.questionText = json.data.text
            this.currentQuestion.questionImage = json.data.image
            this.currentQuestion.possibleAnswers = json.data.possibleAnswers
        },
        async answerClickedHandler(answerSelected) {
            console.log(answerSelected)
            this.answers[this.currentQuestionPosition - 1] = answerSelected
            if (this.currentQuestionPosition >= this.totalNumberOfQuestion)
                this.endQuiz()
            else {
                this.currentQuestionPosition++
                this.loadQuestionByPosition(this.currentQuestionPosition)
            }
        },
        async endQuiz() {
            var playerName = participationStorageService.getPlayerName()
            await quizApiService.saveParticipation(playerName, this.answers)
            console.log("before getting score")
            var score = await quizApiService.getPlayerScore(playerName)
            console.log(this.score)
            console.log(score.data.score)
            console.log("after getting score")
            participationStorageService.saveParticipationScore(score.data.score)
            this.$router.push('/score');
        }
    }
}

</script>

<style>

.questionManager {
    
  max-width: 1000px;
  margin: 0 auto;
  text-align: center;
  display: flex;
  align-items: center;
  justify-content: center
  
}

</style>

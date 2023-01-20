<template>
    <table style="text-align:center">
        <button @click.prevent="goBack">Back</button><br><br>
        <div v-if="question != null">
            <label>
                <h2>Question:</h2>
                Text: <input type="text" v-model="question.text" /><br />
                Title: <input type="text" v-model="question.title" /><br />
                Image: <input type="text" v-model="question.image" /><br />
                Position: <input type="number" min="1" oninput="validity.valid||(value='')" v-model="question.position" /><br />
            </label>
            <br />
            <div class="answer" v-for="(answer, index) in answers" :key="index">
                <label>
                    <h3>Answer {{ index + 1 }}:</h3>
                    Text: <input type="text" v-model="answer.text" /><br />
                    Check correct Answer: <input type="checkbox" id="checkbox" v-model="answer.isCorrect">
                    <p> </p>
                    <button v-if="index > 0" @click.prevent="removeAnswer(index)">Delete Answer {{ index + 1}}</button>
                </label>
            </div>
            <br />
            <div class="modifyQuestion">
                <tr><button @click.prevent="addAnswer" >Add answer</button></tr>
                <br>
                <tr><button @click.prevent="submitQuestion" >Update Question</button></tr>
            </div>
            
            <br>
        </div>
    </table>
</template>

<style>
.answer:not(:first-child) {
    margin-top: 1rem;
}
.answer:last-child {
    margin-bottom: 1rem;
}

.modifyQuestion{
    max-width: 1000px;
    margin: 0 auto;
    text-align: center;
    display: flex;
    align-items: center;
    justify-content: center


}
    
</style>

<script>
import quizApiService from "@/services/QuizApiService";
import adminStorageService from "@/services/AdminStorage";
import ParticipationStorageService from "@/services/ParticipationStorageService";


export default {
    name: "modifyquestion",
    data() {
        return {
            question: new Question(),
            answers: [],
        };
    },
    async created() {
        console.log("Composant Put Question Page 'created'")
        var position = adminStorageService.getQuestionToDetail();
        await this.loadQuestionByPosition(position);
        console.log("Question loaded");
        var id_from_pos = await quizApiService.idByPosition(this.question.position);
        var id_pos = id_from_pos.data.id_question;
        console.log(id_pos);
        ParticipationStorageService.saveIdFromPos(id_pos);

    },
    methods: {
        async loadQuestionByPosition(position) {
            var json = await quizApiService.getQuestion(position)

            this.question.position = position
            this.question.title = json.data.title
            this.question.text = json.data.text
            this.question.image = json.data.image


            for(var a in json.data.possibleAnswers){
                this.answers.push(new Answer(a.text, a.isCorrect))
            }
        },
        goBack() {
            this.$router.push('/editor');
        },
        addAnswer() {
            this.answers.push(new Answer(null,null));
        },
        removeAnswer(index) {
            this.answers.splice(index, 1);
        },
        async submitQuestion() {
            if (confirm("Submit this question ?")) {
                var id_pos = ParticipationStorageService.getIdFromPos();
                console.log("finally got the id below:");
                console.log(id_pos);

                this.question.possibleAnswers = this.answers;


                var token = await adminStorageService.getToken();
                console.log(this.question)

                var response = await quizApiService.updateQuestion(token, id_pos, this.question);


                this.$router.push('/showquestions');
            }
        },
    },
};

export class Question {
    id = "";
    text = "";
    title = "";
    image = "";
    position = "";
    possibleAnswers = "";

    constructor(text, title, image, position) {
        this.text = text;
        this.title = title;
        this.image = image;
        this.position = position;
        this.possibleAnswers = [];
    }

}

export class Answer {
    text = "";
    isCorrect = "";

    constructor(text, isCorrect) {
        if (text == null) this.text = "";
        else this.text = text;

        if(isCorrect == null) this.isCorrect = false;
        else this.isCorrect = isCorrect;
    }

}
</script>

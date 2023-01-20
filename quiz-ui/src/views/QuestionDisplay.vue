<template>
        <div class="question">
            <h1>{{ question.questionTitle }}</h1>
            <img class="img-thumbnail" v-if="question.questionImage" :src="question.questionImage" />
            <h2>{{ question.questionText }}</h2>
            <div class="d-flex flex-column gap-3">
                <div v-for="(answer, index) in question.possibleAnswers" :class="{ active: answer.isActive }" v-bind:id="index">
                    <button @click="$emit('answerSelected', index+1)">{{ answer.text }}</button>
                </div>
            </div>
        </div>
</template>

<script>
export default {
    name: "QuestionDisplay",
    props: {
        question: {
            type: Object
        }
    },
    emits: ["answerSelected"]
}
</script>

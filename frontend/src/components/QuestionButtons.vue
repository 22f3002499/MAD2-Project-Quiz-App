<template>
  <BContainer class="overflow-y-auto hide-scrollbar" style="max-height: 400px">
    <BRow cols="5" class="ms-5" v-if="store.questionAndOptions">
      <BButton
        :variant="getButtonVariant(ques)"
        v-for="(ques, index) in store.questionAndOptions"
        :key="ques.id"
        :id="ques.id"
        class="p-3 m-1 text-center rounded px-2"
        @click="() => setCurrentQuestion(ques)"
        >{{ index + 1 }}</BButton
      >
    </BRow>
  </BContainer>
</template>

<script setup>
import { useStartQuizStore } from "@/stores/startQuizStore";
import { toRaw } from "vue";

const store = useStartQuizStore();

function setCurrentQuestion(ques) {
  store.currentQuestion = toRaw(ques);
  const visitedQuestions = store.visitedQuestions;
  const currentQuestionId = store.currentQuestion?.id.toString();
  if (!visitedQuestions.includes(currentQuestionId)) {
    store.visitedQuestions = [...visitedQuestions, currentQuestionId];
  }
}

function getButtonVariant(ques) {
  const questionId = ques.id?.toString();
  const answeredQuestions = Object.keys(store.userAnswers);
  const visitedQuestions = store.visitedQuestions;

  if (visitedQuestions.includes(questionId)) {
    if (
      answeredQuestions.includes(questionId) &&
      store.userAnswers[questionId]?.length > 0
    ) {
      return "success";
    } else {
      return "danger";
    }
  } else {
    return "outline-dark";
  }
}
</script>

<style scoped>
.hide-scrollbar {
  -webkit-scrollbar {
    display: none;
  }
  -ms-overflow-style: none;
  scrollbar-width: none;
}
</style>

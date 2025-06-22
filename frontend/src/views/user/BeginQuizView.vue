<template>
  <BContainer fluid class="px-5">
    <BRow class="mt-2 mx-0" style="max-height: 775px; height: 775px">
      <BCol cols="8">
        <BRow cols="1">
          <QuizQuestionAndOptions />
        </BRow>
      </BCol>
      <BCol class="p-0" cols="4">
        <BContainer fluid class="">
          <BRow cols="1">
            <BCol class="mb-3 d-flex justify-content-center">
              <!-- TIME LEFT COUNTER -->
              <BBadge class="text-center mt-3 pt-2 px-3" variant="secondary">
                <h5 class="text-center">
                  Time Left: <span>{{ timer.formattedTime }}</span>
                </h5>
              </BBadge>
            </BCol>
            <BCol class="px-0 mt-2">
              <!-- INDICATOR -->
              <h4 class="text-center">Question Indicators</h4>
              <QuestionIndicator />
            </BCol>
            <BCol class="mt-2 px-0">
              <!-- QUESTION BUTTONS -->
              <h4 class="text-center mb-3">Questions</h4>
              <QuestionButtons />
            </BCol>
            <BCol class="mt-2 d-flex justify-content-center align-items-center">
              <BButton
                variant="outline-secondary"
                class="p-2 px-3 mx-auto fw-bold fs-5"
                @click="submitQuiz"
                >Submit</BButton
              >
            </BCol>
          </BRow>
        </BContainer>
      </BCol>
    </BRow>
  </BContainer>
</template>

<script setup>
import { onBeforeMount, onMounted } from "vue";
import { useStartQuizStore } from "@/stores/startQuizStore";
import { useRoute, useRouter } from "vue-router";

import QuestionIndicator from "@/components/QuestionIndicator.vue";
import QuestionButtons from "@/components/QuestionButtons.vue";
import QuizQuestionAndOptions from "@/components/QuizQuestionAndOptions.vue";
import { useTimer } from "@/composables/useTimer";

const startQuizStore = useStartQuizStore();
const route = useRoute();
const router = useRouter();

onBeforeMount(async () => {
  await startQuizStore.startQuiz(route.params.quizId);

  if (startQuizStore.questionAndOptions.length > 0) {
    startQuizStore.currentQuestion = startQuizStore.questionAndOptions[0];
  }
});

const timer = useTimer(startQuizStore.quizDuration, () => {
  submitQuiz();
});

const submitQuiz = () => {
  startQuizStore.submitQuiz(route.params.quizId);
  router.push({ path: "/" });
};

onMounted(() => {
  timer.startTimer();
});
</script>

<template>
  <h2 class="fw-bold text-center mt-5">Upcoming Quizzes</h2>
  <div
    class="d-flex px-5 py-2 flex-column align-items-center justify-content-center"
    style="height: 65vh"
  >
    <QuizTable :quizzes="quizStore.userQuizzes" class="mh-100" />
  </div>
</template>

<script setup>
import { useQuizStore } from "@/stores/dbQuizStore";
import { onBeforeMount } from "vue";
import QuizTable from "@/components/QuizTable.vue";

const quizStore = useQuizStore();

onBeforeMount(async () => {
  await quizStore.getUserQuizzes();
});
</script>

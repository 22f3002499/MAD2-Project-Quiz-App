<template>
  <h2 class="fw-bold text-center mt-4">Upcoming Quizzes</h2>
  <BContainer style="max-width: 70vw; max-height: 70vh" class="mt-3">
    <BCard class="mb-4 p-2">
      <SearchBar
        :items="store.userQuizzes"
        :sortByFields="['title', 'description', 'start_datetime']"
        @update="handleUpdate"
      />
    </BCard>
    <BContainer class="overflow-y-scroll px-2" style="max-height: inherit">
      <QuizCards :userQuizzes="processedQuizzes" />
    </BContainer>
  </BContainer>
</template>

<script setup>
import SearchBar from "@/components/SearchBar.vue";
import QuizCards from "@/components/user/QuizCards.vue";
import { useQuizStore } from "@/stores/dbQuizStore";
import { onBeforeMount, ref } from "vue";

const store = useQuizStore();
const processedQuizzes = ref([]);

onBeforeMount(async () => {
  await store.getUserQuizzes();
});

const handleUpdate = (values) => {
  processedQuizzes.value = values;
};
</script>

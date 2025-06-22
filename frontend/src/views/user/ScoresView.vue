<template>
  <h2 class="fw-bold text-center mt-5">Scores</h2>
  <div
    class="d-flex px-5 py-2 flex-column align-items-center justify-content-center"
    style="height: 70vh"
  >
    <ScoresTable :scores="store.scores" />
  </div>
</template>

<script setup>
import { useScoresStore } from "@/stores/scoresStore";
import { onBeforeMount, onMounted } from "vue";

const store = useScoresStore();
onBeforeMount(async () => {
  await store.getScores();
});
</script>

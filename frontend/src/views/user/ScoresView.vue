<template>
  <h2 class="fw-bold text-center mt-5">Scores</h2>
  <BContainer style="max-width: 70vw; max-height: 70vh" class="mt-4">
    <BCard class="mb-4 p-2">
      <SearchBar :items="store.scores" @update="handleSearchUpdate" />
    </BCard>

    <BContainer class="overflow-y-scroll px-2" style="max-height: inherit">
      <ScoreCards :scores="processedScores || []" />
    </BContainer>
  </BContainer>
</template>

<script setup>
import ScoreCards from "@/components/user/ScoreCards.vue";
import { useScoresStore } from "@/stores/scoresStore";
import { onBeforeMount, ref } from "vue";

const store = useScoresStore();
const processedScores = ref([]);
onBeforeMount(async () => {
  await store.getScores();
});

const handleSearchUpdate = (values) => {
  processedScores.value = values;
};
</script>

<template>
  <h2 class="fw-bold text-center mt-5">Scores</h2>
  <BContainer style="max-width: 70vw; max-height: 70vh" class="mt-4">
    <BCard class="mb-4 p-2" body-class="d-flex">
      <SearchBar
        :items="store.scores"
        @update="handleSearchUpdate"
        class="flex-fill"
      />
      <BButton variant="outline-secondary ms-4" @click="triggerReport"
        >Get Monthly Report</BButton
      >
    </BCard>

    <BContainer class="overflow-y-scroll px-2" style="max-height: inherit">
      <ScoreCards
        v-if="processedScores.length > 0"
        :scores="processedScores || []"
      />
      <h3 v-else class="text-center">No Scores Found</h3>
    </BContainer>
  </BContainer>
</template>

<script setup>
import ScoreCards from "@/components/user/ScoreCards.vue";
import { useApi } from "@/composables/useApi";
import { useToast } from "@/composables/useToast";
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

const { get } = useApi();
const toast = useToast();
const triggerReport = async () => {
  try {
    const response = await get("/user/monthly-report/");
    toast.createSuccessToast(response?.message, "");
  } catch (error) {
    toast.createErrorToast(
      error.code,
      JSON.stringify(error?.response?.data) || error?.message,
    );
  }
};
</script>

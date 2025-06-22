<template>
  <BTable
    hover
    responsive
    sticky-header
    :items="props.scores"
    :fields="fields"
    class="mh-100"
  >
    <template #cell(actions)="{ item }">
      <BButtonGroup>
        <BButton
          variant="outline-dark"
          @click="store.getUserAnswers(item.id)"
          v-b-modal.user-answers
          >Review Answers</BButton
        >
        <BButton
          variant="outline-dark"
          @click="store.downloadUserAnswers(item.id)"
          ><i class="bi bi-arrow-down-circle"></i
        ></BButton>
      </BButtonGroup>
    </template>
  </BTable>

  <BModal id="scores-detail-modal" scrollable title="Score Details" ok-only>
  </BModal>

  <BModal id="user-answers" scrollable title="User Answers" ok-only size="xl">
    <ReviewScoresComponent />
  </BModal>
</template>

<script setup>
import { useScoresStore } from "@/stores/scoresStore";
import { onMounted } from "vue";
import { useApi } from "@/composables/useApi";

import ReviewScoresComponent from "./ReviewScoresComponent.vue";

const store = useScoresStore();

const props = defineProps({
  scores: Array,
});

const formatDateTime = (value) => {
  if (!value) return "N/A";
  const date = new Date(value * 1000);
  return date;
};

const formatNumber = (value) => {
  return value.toFixed(2);
};
const fields = [
  { key: "id", label: "ID" },
  { key: "quiz_title" },
  { key: "quiz_total_marks", label: "Quiz Marks" },
  { key: "score", formatter: formatNumber },
  { key: "percentage_score", label: "%age Score", formatter: formatNumber },
  { key: "submit_datetime", label: "Submitted At", formatter: formatDateTime },
  {
    key: "actions",
  },
];

const { get } = useApi();
</script>

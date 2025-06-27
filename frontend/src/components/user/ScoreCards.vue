<template>
  <BRow cols="2" md="6" class="g-4">
    <BCol v-for="score in enrichedScores" :key="score.id">
      <BCard
        header-border-variant="white"
        header-bg-variant="light-subtle"
        footer-border-variant="white"
        footer-bg-variant="white"
      >
        <template #header>
          <BContainer>
            <BBadge variant="primary" class="me-2">ID: {{ score.id }}</BBadge>
            <BBadge variant="info">{{ score.chapter_title }}</BBadge>
          </BContainer>
        </template>

        <BCardText>
          <span
            ><b>{{ score.quiz_title }}</b></span
          >
        </BCardText>

        <BRow cols="4">
          <BCol>
            <div class="d-flex flex-column align-items-center">
              <b>{{ score.quiz_total_marks }}</b>
              <span class="text-secondary small">Total Marks</span>
            </div>
          </BCol>

          <BCol>
            <div class="d-flex flex-column align-items-center">
              <b>{{ score.formattedScore }}</b>
              <span class="text-secondary small">Your Score</span>
            </div>
          </BCol>

          <BCol>
            <div class="d-flex flex-column align-items-center">
              <BBadge :class="score.percentageBadgeVariant">
                {{ score.formattedPercentage }}%
              </BBadge>
              <span class="text-secondary small">Percentage</span>
            </div>
          </BCol>

          <BCol>
            <div class="d-flex flex-column align-items-center">
              <BBadge :variant="score.statusVariant">
                {{ score.status }}
              </BBadge>
              <span class="text-secondary small">Status</span>
            </div>
          </BCol>
        </BRow>

        <template #footer>
          <div class="d-flex mb-1 align-items-center">
            <span class="small text-secondary">{{
              getDateTime(score.submit_datetime)
            }}</span>
            <BButtonGroup class="ms-auto">
              <BButton
                v-b-modal.user-answers
                variant="secondary"
                size="sm"
                @click="store.getUserAnswers(score.id)"
                >Review Answers</BButton
              >
              <BButton
                variant="outline-secondary"
                size="sm"
                @click="store.downloadUserAnswers(score.id)"
                ><i class="bi bi-arrow-down-circle"></i
              ></BButton>
            </BButtonGroup>
          </div>
        </template>
      </BCard>
    </BCol>
  </BRow>

  <BModal
    id="user-answers"
    scrollable
    title="User Answers"
    ok-only
    size="xl"
    header-variant="primary"
  >
    <ReviewScoresComponent />
  </BModal>
</template>

<script setup>
import { useScoresStore } from "@/stores/scoresStore";
import { computed } from "vue";

const props = defineProps({
  scores: {
    type: Array,
    required: true,
  },
});

const store = useScoresStore();

const enrichedScores = computed(() => {
  return props.scores.map((score) => {
    const formattedScore = score.score.toFixed(2);
    const formattedPercentage = score.percentage_score.toFixed(2);
    const isPassing = score.percentage_score >= score.passing_percentage;

    let percentageBadgeVariant;
    if (!isPassing) {
      percentageBadgeVariant = "danger";
    } else if (score.percentage_score < 40) {
      percentageBadgeVariant = "warning";
    } else if (score.percentage_score < 70) {
      percentageBadgeVariant = "primary";
    } else {
      percentageBadgeVariant = "success";
    }
    percentageBadgeVariant = `bg-${percentageBadgeVariant}-subtle text-${percentageBadgeVariant}`;

    return {
      ...score,
      formattedScore,
      formattedPercentage,
      status: isPassing ? "Pass" : "Fail",
      statusVariant: isPassing ? "success" : "danger",
      percentageBadgeVariant,
    };
  });
});

const getDateTime = (value) => {
  if (!value) return "N/A";
  const datetime = new Date(value * 1000);
  const formattedDate = datetime.toLocaleString("en-US", {
    month: "short",
    day: "numeric",
    year: "numeric",
    hour: "numeric",
    minute: "numeric",
    second: "numeric",
    hour12: true,
  });
  return formattedDate;
};
</script>

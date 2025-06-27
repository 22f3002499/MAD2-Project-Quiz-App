<template>
  <h2 class="fw-bold text-center mt-4">Statistics</h2>

  <!-- TOP BAR STATS -->
  <BContainer class="mt-3">
    <BCardGroup deck>
      <BCard
        class="d-flex flex-column align-items-center text-center mx-4 py-2"
      >
        <i class="bi bi-card-list fs-3 text-primary mb-2"></i>
        <h3>{{ store.stats.total_attempts }}</h3>
        <span class="text-secondary">Total Attempts</span>
      </BCard>

      <BCard
        class="d-flex flex-column align-items-center text-center mx-4 py-2"
      >
        <i class="bi bi-trophy fs-3 text-success mb-2"></i>
        <h3>{{ store.stats.average_score }}</h3>
        <span class="text-secondary">Average Score</span>
      </BCard>

      <BCard
        class="d-flex flex-column align-items-center text-center mx-4 py-2"
      >
        <i class="bi bi-percent fs-3 text-info mb-2"></i>
        <h3>{{ store.stats.pass_rate }}</h3>
        <span class="text-secondary">Pass Rate</span>
      </BCard>

      <BCard
        class="d-flex flex-column align-items-center text-center mx-4 py-2"
      >
        <i class="bi bi-book fs-3 text-warning mb-2"></i>
        <h3>{{ store.stats.total_subjects }}</h3>
        <span class="text-secondary">Subjects</span>
      </BCard>
    </BCardGroup>
  </BContainer>

  <BContainer class="mt-5">
    <BRow>
      <!-- SUBJECT PERFORMANCE -->
      <!-- LEFT CARD STATS -->
      <BCol cols="8">
        <BCard>
          <div class="fw-bold fs-5 ms-3">Subject-wise Performance</div>

          <BListGroup flush style="max-height: 500px" class="overflow-y-scroll">
            <BListGroupItem
              v-for="subStats in store.stats?.subject_wise_stats"
              class="border-0"
            >
              <div class="d-flex">
                <div class="fw-bold">{{ subStats.subject_name }}</div>

                <div class="ms-auto">
                  <BBadge variant="primary" class="me-2"
                    >{{ subStats.attempts }} attempts</BBadge
                  >
                  <BBadge :variant="getVariant(subStats.pass_rate)"
                    >{{ subStats.pass_rate }}%</BBadge
                  >
                </div>
              </div>

              <BProgress
                :variant="getVariant(subStats.average_score)"
                :value="subStats.average_score"
                class="mt-2"
                height="6px"
              ></BProgress>

              <p class="text-secondary small mb-3">
                Average Score : {{ subStats.average_score }}
              </p>
            </BListGroupItem>
          </BListGroup>
        </BCard>
      </BCol>

      <!-- RECENT ATTEMPTS -->
      <!-- RIGHT CARD STATS -->
      <BCol cols="4">
        <BCard>
          <div class="fw-bold fs-5 ms-3">Recent Attempts</div>

          <BListGroup flush class="overflow-y-scroll" style="max-height: 500px">
            <BListGroupItem
              v-for="attempt in store.stats?.recent_attempts"
              class="mb-3 border-0"
            >
              <div class="d-flex justify-content-between">
                <div class="fw-bold">{{ attempt.quiz_title }}</div>
                <BBadge
                  :variant="attempt.passed ? 'success' : 'danger'"
                  style="height: fit-content"
                  >{{ attempt.passed ? "Passed" : "Failed" }}</BBadge
                >
              </div>
              <span class="text-secondary">{{ attempt.subject }}</span>

              <div class="d-flex small text-secondary mt-3">
                <span class=""
                  >{{ attempt.score }} / {{ attempt.total_marks }} ({{
                    attempt.percentage
                  }}%)</span
                >

                <span class="ms-auto">{{ attempt.date }}</span>
              </div>
            </BListGroupItem>
          </BListGroup>
        </BCard>
      </BCol>
    </BRow>
  </BContainer>

  <!-- PERFORMANCE INSIGHTS -->
  <!-- BOTTOM CARD -->
  <BContainer class="my-5">
    <BCard>
      <div class="fw-bold fs-5">Performance Insights</div>
      <BRow cols="3" class="mt-3 px-3 mb-2">
        <BCol class="d-flex flex-column text-center">
          <i class="bi bi-graph-up fs-3 text-success"></i>
          <div class="fw-bold">Strongest Subject</div>
          <div class="text-secondary">
            {{ strongestSubject.name }} ({{ strongestSubject.pass_rate }}% pass
            rate)
          </div>
        </BCol>

        <BCol class="d-flex flex-column text-center">
          <i class="bi bi-graph-down fs-3 text-danger"></i>
          <div class="fw-bold">Needs Improvement</div>
          <div class="text-secondary">
            {{ weakestSubject.name }}
          </div>
        </BCol>

        <BCol class="d-flex flex-column text-center">
          <i class="bi bi-calendar-check fs-3 text-info"></i>
          <div class="fw-bold">Most Active Subject</div>
          <div class="text-secondary">
            {{ mostActiveSubject.name }} ({{ mostActiveSubject.attempts }}
            attempts)
          </div>
        </BCol>
      </BRow>
    </BCard>
  </BContainer>
</template>

<script setup>
import { useUserStatsStore } from "@/stores/userStatsStore";
import { onBeforeMount, ref, toRaw, computed } from "vue";

const store = useUserStatsStore();

onBeforeMount(async () => {
  await store.getStats();
});

const getVariant = (passRate) => {
  if (passRate > 90) return "success";
  else if (passRate > 70) return "primary";
  else if (passRate > 50) return "warning";
  else return "danger";
};

const strongestSubject = computed(() => {
  const userStats = ref(toRaw(store.stats));
  if (!userStats.value?.subject_wise_stats?.length)
    return { name: "N/A", pass_rate: 0 };

  const strongest = userStats.value.subject_wise_stats.reduce(
    (prev, current) => (prev.pass_rate > current.pass_rate ? prev : current),
  );
  return { name: strongest.subject_name, pass_rate: strongest.pass_rate };
});

const weakestSubject = computed(() => {
  const userStats = ref(toRaw(store.stats));
  if (!userStats.value?.subject_wise_stats?.length) return { name: "N/A" };

  const weakest = userStats.value.subject_wise_stats.reduce((prev, current) =>
    prev.pass_rate < current.pass_rate ? prev : current,
  );
  return { name: weakest.subject_name };
});

const mostActiveSubject = computed(() => {
  const userStats = ref(toRaw(store.stats));
  if (!userStats.value?.subject_wise_stats?.length)
    return { name: "N/A", attempts: 0 };

  const mostActive = userStats.value.subject_wise_stats.reduce(
    (prev, current) => (prev.attempts > current.attempts ? prev : current),
  );
  return { name: mostActive.subject_name, attempts: mostActive.attempts };
});
</script>

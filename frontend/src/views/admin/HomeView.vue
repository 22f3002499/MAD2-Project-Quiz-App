<template>
  <h1 class="text-center my-4">Dashboard</h1>

  <BRow class="px-5" v-if="stats">
    <BCol class="bg-light-subtle p-5 me-4 pt-4">
      <b class="fs-5 mb-2 d-block">Subject Performance</b>
      <BTable
        hover
        outlined
        borderless
        responsive
        sticky-header
        head-variant="dark"
        :items="stats.subject_performance"
        :fields="[
          { key: 'subject_name', label: 'Subject Name' },
          {
            key: 'pass_rate',
            sortable: true,
            formatter: (value) => value + '%',
          },
          {
            key: 'average_percentage_score',
            label: 'Average Score',
            sortable: true,
            formatter: (value) => value + '%',
          },
          {
            key: 'total_quizzes',
            sortable: true,
          },
        ]"
        style="max-height: 500px"
      >
      </BTable>
    </BCol>
    <BCol class="bg-light-subtle p-5 px-4 me-4 pt-4 rounded">
      <b class="fs-5 mb-2 d-block">Top Performers</b>
      <BTable
        hover
        outlined
        borderless
        responsive="sm"
        sticky-header
        head-variant="dark"
        :items="stats.top_performers"
        :fields="[
          { key: 'rank', sortable: true },
          {
            key: 'average_percentage_score',
            sortable: true,
            formatter: (value) => value + '%',
          },
          {
            key: 'pass_rate',
            sortable: true,
            formatter: (value) => value + '%',
          },
          { key: 'unique_quizzes_attempted', label: 'Quizzes Attempted' },
        ]"
        style="max-height: 500px"
        class="mb-0"
      >
      </BTable>
    </BCol>
    <BCol cols="4">
      <BRow class="bg-light-subtle rounded p-2 py-3">
        <BCol>
          <BCard body-class="d-flex">
            <div
              class="rounded-circle bg-primary d-flex justify-content-center align-items-center"
              style="height: 50px; width: 50px"
            >
              <i class="bi bi-person-circle text-white fs-3"></i>
            </div>

            <div class="ms-3">
              <h5 class="text-center">{{ stats.total_users }}</h5>
              <span class="text-secondary">Total Users</span>
            </div>
          </BCard>
          <BCard body-class="d-flex" class="mt-3">
            <div
              class="rounded-circle bg-warning d-flex justify-content-center align-items-center"
              style="height: 50px; width: 50px"
            >
              <i class="bi bi-clipboard-data text-white fs-3"></i>
            </div>

            <div class="ms-3">
              <h5 class="text-center">{{ stats.total_quizzes }}</h5>
              <span class="text-secondary">Total Quizzes</span>
            </div>
          </BCard>
        </BCol>
        <BCol>
          <BCard body-class="d-flex" class="">
            <div
              class="rounded-circle bg-secondary d-flex justify-content-center align-items-center"
              style="height: 50px; width: 50px"
            >
              <i class="bi bi-bar-chart-fill text-white fs-3"></i>
            </div>

            <div class="ms-4">
              <h5 class="text-center">{{ stats.total_quiz_attempts }}</h5>
              <span class="text-secondary">Total Attempts</span>
            </div>
          </BCard>
          <BCard body-class="d-flex" class="mt-3">
            <div
              class="rounded-circle bg-danger d-flex justify-content-center align-items-center"
              style="height: 50px; width: 50px"
            >
              <i class="bi bi-book-fill text-white fs-3"></i>
            </div>

            <div class="ms-4">
              <h5 class="text-center">{{ stats.total_subjects }}</h5>
              <span class="text-secondary">Total Subjects</span>
            </div>
          </BCard>
        </BCol>
      </BRow>

      <BRow class="mt-5 bg-light-subtle p-2 py-3 rounded">
        <BCol>
          <BCard body-class="me-2">
            <div class="fw-medium text-secondary">Average Quiz Score</div>
            <h3 class="text-primary mt-2">{{ stats.average_quiz_score }}</h3>
            <BProgress :value="stats.average_quiz_score"></BProgress>
            <div class="text-secondary mt-1">
              Based on {{ stats.total_quiz_attempts }} attempts
            </div>
          </BCard>
          <BCard body-class="me-2" class="mt-3">
            <div class="fw-medium text-secondary">Average Pass Rate</div>
            <h3 class="text-success mt-2">{{ stats.average_pass_rate }}</h3>
            <BProgress
              :value="stats.average_pass_rate"
              variant="success"
            ></BProgress>
            <div class="text-secondary mt-1">Students passing quizzes</div>
          </BCard>
        </BCol>

        <BCol>
          <BCard body-class="me-2" class="">
            <div class="fw-medium text-secondary">Active Users Today</div>
            <h3 class="text-info mt-2">{{ stats.active_users_today }}</h3>
            <BProgress
              :value="stats.active_users_today"
              variant="info"
            ></BProgress>
            <div class="text-secondary mt-1">
              {{ (stats.active_users_today / stats.total_users) * 100 }}% of
              total users
            </div>
          </BCard>
          <BCard body-class="me-2" class="mt-3">
            <div class="fw-medium text-secondary">Pending Quizzes Today</div>
            <h3 class="text-danger mt-2">{{ stats.pending_quizzes_today }}</h3>
            <BProgress
              :value="stats.pending_quizzes_today"
              variant="danger"
            ></BProgress>
            <div class="text-secondary mt-1">Quizzes with no attempts</div>
          </BCard>
        </BCol>
      </BRow>
    </BCol>
  </BRow>
</template>

<script setup>
import { useApi } from "@/composables/useApi";
import { onBeforeMount, ref } from "vue";

const stats = ref(null);

onBeforeMount(async () => {
  const { get } = useApi();
  stats.value = await get("/admin/dashboard/");
});
</script>

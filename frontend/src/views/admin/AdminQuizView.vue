<template>
  <h2 class="fw-bold text-center mt-5">Quizzes</h2>
  <BContainer
    style="max-width: 70vw; max-height: 70vh"
    class="mt-4 overflow-y-scroll"
  >
    <SearchBar
      :items="quizStore.allQuizzes"
      @update="handleSearchUpdate"
      class="sticky-top"
    />
    <BRow cols="2">
      <BCol v-for="quiz in processedQuizzes" class="mt-4">
        <BCard
          header-bg-variant="light-subtle"
          footer-bg-variant="white"
          class="h-100"
        >
          <template #header>
            <div class="d-flex align-items-center">
              <span class="fw-bold">{{ quiz.title }}</span>
              <BBadge variant="primary" class="ms-auto"
                >ID: {{ quiz.id }}</BBadge
              >
            </div>
          </template>

          <BRow>
            <!-- FIRST COLUMN -->
            <BCol cols="7">
              <BRow class="ms-3">
                <!-- DURATION -->
                <BCol class="d-flex align-items-center justify-content-start">
                  <i class="bi bi-clock text-warning"></i>
                  <div class="ms-3">
                    <small class="d-block">Duration</small>
                    <strong>{{ quiz.duration }} mins</strong>
                  </div>
                </BCol>
              </BRow>

              <BRow class="mt-2 ms-3">
                <!-- START DATETIME -->
                <BCol class="d-flex align-items-center justify-content-start">
                  <i class="bi bi-calendar text-primary"></i>
                  <div class="ms-3">
                    <small class="d-block">Start Date & Time</small>
                    <strong>{{ getDateTime(quiz.start_datetime) }}</strong>
                  </div>
                </BCol>
              </BRow>

              <BRow class="mt-2 ms-3">
                <!-- TOTAL QUESTIONS -->
                <BCol class="d-flex align-items-center justify-content-start">
                  <i class="bi bi-question-lg text-danger"></i>
                  <div class="ms-3">
                    <small class="d-block">Total Questions</small>
                    <strong>{{ quiz.total_questions }} questions</strong>
                  </div>
                </BCol>
              </BRow>
            </BCol>

            <!-- SECOND COLUMN -->
            <BCol cols="5">
              <BRow>
                <!-- TOTAL MARKS -->
                <BCol class="d-flex align-items-center justify-content-start">
                  <i class="bi bi-award text-success"></i>
                  <div class="ms-3">
                    <small class="d-block">Total Marks</small>
                    <strong>{{ quiz.total_marks }} points</strong>
                  </div>
                </BCol>
              </BRow>

              <BRow class="mt-2">
                <!-- TOTAL QUESTIONS -->
                <BCol class="d-flex align-items-center justify-content-start">
                  <i class="bi bi-percent text-info"></i>
                  <div class="ms-3">
                    <small class="d-block">Passing Percentage</small>
                    <strong>{{ quiz.passing_percentage }} %</strong>
                  </div>
                </BCol>
              </BRow>

              <BRow class="mt-2">
                <BCol class="d-flex align-items-center justify-content-start">
                  <!-- ATTMEPTS ALLOWED -->
                  <i class="bi bi-repeat text-warning"></i>
                  <div class="ms-3">
                    <small class="d-block">Attempts Allowed</small>
                    <strong>{{ quiz.attempts_allowed }} attempts</strong>
                  </div>
                </BCol>
              </BRow>
            </BCol>
          </BRow>

          <!-- CHAPTER AND SUBJECT CARD -->
          <BRow class="mt-5 mx-1">
            <!-- CHAPTER SUB CARD -->
            <BCol cols="6">
              <BCard class="bg-light h-100">
                <div class="d-flex align-items-center">
                  <div class="text-primary">
                    <i class="bi bi-book"></i>
                    <strong class="ms-3">Chapter</strong>
                  </div>

                  <BBadge class="bg-secondary-subtle text-secondary ms-auto"
                    >ID: {{ quiz.chapter.id }}</BBadge
                  >
                </div>

                <h6 class="fw-bold mt-3">{{ quiz.chapter.title }}</h6>

                <p class="small">{{ quiz.chapter.description }}</p>
              </BCard>
            </BCol>

            <!-- SUBJECT SUB CARD -->
            <BCol cols="6">
              <BCard class="bg-light h-100">
                <div class="d-flex align-items-center">
                  <div class="text-success">
                    <i class="bi bi-book"></i>
                    <strong class="ms-3">Subject</strong>
                  </div>

                  <BBadge class="bg-secondary-subtle text-secondary ms-auto">
                    ID: {{ quiz.subject.id }}
                  </BBadge>
                </div>

                <h6 class="fw-bold mt-3">{{ quiz.subject.title }}</h6>

                <p class="small">{{ quiz.subject.description }}</p>
              </BCard>
            </BCol>
          </BRow>

          <template #footer>
            <div class="text-end">
              <BButton
                size="sm"
                variant="primary"
                class="me-2"
                v-b-modal.view-questions-and-options
                @click="
                  () => {
                    currentQuiz = quiz;
                    quizStore.getQuizQuestionsAndOptions(quiz.id);
                  }
                "
                >View Questions & Options</BButton
              >
              <BButton
                size="sm"
                variant="warning"
                class="me-2"
                :disabled="hasQuizStarted(quiz.start_datetime)"
                v-b-modal.edit-quiz
                @click="currentQuiz = quiz"
                >Edit</BButton
              >
              <BButton
                size="sm"
                variant="danger"
                :disabled="hasQuizStarted(quiz.start_datetime)"
                @click="
                  () => {
                    quizStore.removeQuiz(quiz.id);
                    quizStore.fetchAllQuizzes();
                  }
                "
                >Remove</BButton
              >
            </div>
          </template>
        </BCard>
      </BCol>
    </BRow>
  </BContainer>

  <FormModal
    id="edit-quiz"
    title="Edit Quiz"
    header-variant="warning"
    @submit="handleEditQuizSubmit"
    :initialData="quizStore.getQuizById(currentQuizId)"
    :formSchema="quizSchema"
  >
    <QuizForm />
  </FormModal>

  <BModal
    id="view-questions-and-options"
    title="View Questions"
    ok-only
    size="xl"
  >
    <QuizQuestionsAndOptionsCRUD
      v-if="currentQuiz"
      :quizStarted="hasQuizStarted(currentQuiz?.start_datetime)"
      @refetchQuestionsAndOptions="
        quizStore.getQuizQuestionsAndOptions(currentQuizId)
      "
    />
  </BModal>
</template>

<script setup>
import QuizForm from "@/components/admin/QuizForm.vue";
import FormModal from "@/components/FormModal.vue";
import { quizSchema } from "@/utils/formSchemas";

import { useQuizStore } from "@/stores/dbQuizStore";
import { computed, onBeforeMount, provide, ref, watch } from "vue";
import QuizQuestionsAndOptionsCRUD from "@/components/admin/QuizQuestionsAndOptionsCRUD.vue";

const quizStore = useQuizStore();
const processedQuizzes = ref([]);
const currentQuiz = ref();
const currentQuizId = computed(() => currentQuiz.value?.id || null);

// provide this value for quizform to fetch chapters
const currentSubjectId = computed(() => currentQuiz.value?.subject?.id || null);
provide("currentSubjectId", currentSubjectId);

const handleSearchUpdate = (values) => {
  processedQuizzes.value = values;
};

onBeforeMount(async () => {
  await quizStore.fetchAllQuizzes();
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
    hour12: false,
  });
  return formattedDate;
};

const hasQuizStarted = (quizStartDatetime) => {
  const quizDatetime = new Date(quizStartDatetime * 1000);
  const currentDatetime = new Date();

  return currentDatetime > quizDatetime;
};

const handleEditQuizSubmit = async (formData) => {
  console.log(formData);
  await quizStore.editQuiz(currentQuizId.value, formData);
};
</script>

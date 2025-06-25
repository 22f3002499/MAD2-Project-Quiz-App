<template>
  <BRow class="g-3">
    <BCol
      cols="12"
      v-for="quiz in props.userQuizzes"
      :key="quiz.id"
      class="d-flex"
    >
      <BCard
        :title="quiz.title"
        header-border-variant="light"
        header-bg-variant="light-subtle"
        footer-border-variant="white"
        footer-bg-variant="white"
        footer-class="ps-0 ms-0"
        class="p-2 h-100 w-100"
      >
        <template #header>
          <BRow cols="2">
            <BCol>
              <BBadge variant="primary" pill class="me-2">{{
                quiz.subject_title
              }}</BBadge>
              <BBadge variant="info" pill>{{ quiz.chapter_title }}</BBadge>
            </BCol>
            <BCol class="text-end">
              <BBadge variant="warning" pill>{{
                getDateTime(quiz.start_datetime)
              }}</BBadge>
            </BCol>
          </BRow>
        </template>
        <BCardText>{{ quiz.description }}</BCardText>

        <template #footer>
          <div class="d-flex align-items-center justify-content-start">
            <BCol cols="2">
              <div class="d-flex flex-column align-items-center">
                <i class="bi bi-clock"></i>
                <span
                  ><b>{{ quiz.duration }}</b> mins</span
                >
              </div>
            </BCol>

            <BCol cols="2">
              <div class="d-flex flex-column align-items-center">
                <i class="bi bi-question-circle"></i>
                <span
                  ><b>{{ quiz.total_questions }}</b> questions</span
                >
              </div>
            </BCol>

            <BCol cols="2">
              <div class="d-flex flex-column align-items-center">
                <i class="bi bi-award"></i>
                <span
                  ><b>{{ quiz.total_marks }}</b> marks</span
                >
              </div>
            </BCol>

            <BCol cols="2">
              <div class="d-flex flex-column align-items-center">
                <i class="bi bi-calendar"></i>
                <span
                  ><b>{{ getDate(quiz.start_datetime) }}</b></span
                >
              </div>
            </BCol>

            <BCol cols="4">
              <BButton
                v-if="
                  quizReadyStates[quiz.id] ||
                  !isStartDisabled(quiz.start_datetime)
                "
                variant="success"
                @click="
                  $router.push({
                    name: 'begin-quiz',
                    params: { quizId: quiz.id },
                  })
                "
              >
                <i class="bi bi-play-fill"></i> Start Quiz
              </BButton>

              <QuizStartTimeProgress
                v-else
                :quizStartDatetime="quiz.start_datetime"
                @quiz-ready="handleQuizReady(quiz.id)"
              />
            </BCol>
          </div>
        </template>
      </BCard>
    </BCol>
  </BRow>
</template>

<script setup>
import { ref } from "vue";
import QuizStartTimeProgress from "./QuizStartTimeProgress.vue";

const props = defineProps({
  userQuizzes: {
    type: Array,
    required: true,
  },
});

const quizReadyStates = ref({});

const handleQuizReady = (quizId) => {
  quizReadyStates.value[quizId] = true;
};

const getDateTime = (value) => {
  if (!value) return "N/A";
  const datetime = new Date(value * 1000);
  const formattedDate = datetime.toLocaleString("en-US", {
    month: "numeric",
    day: "numeric",
    year: "numeric",
    hour: "numeric",
    minute: "numeric",
    second: "numeric",
    hour12: true,
  });
  return formattedDate;
};

const getDate = (value) => {
  if (!value) return "N/A";
  const datetime = new Date(value * 1000);
  const formattedDate = datetime.toLocaleString("en-US", {
    month: "short",
    day: "numeric",
  });

  return formattedDate;
};
const isStartDisabled = (quizStartDatetime) => {
  const quizStartDate = new Date(quizStartDatetime * 1000);
  const currentDate = new Date();
  return quizStartDate > currentDate;
};
</script>

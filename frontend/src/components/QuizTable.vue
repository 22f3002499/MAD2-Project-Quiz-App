<template>
  <BTable
    hover
    responsive
    sticky-header
    :items="props.quizzes"
    :fields="fields"
  >
    <template #cell(actions)="{ item }">
      <BButton
        variant="success"
        class="me-3"
        @click="$router.push({ path: `/begin-quiz/${item.id}/` })"
        :disabled="isStartDisabled(item.start_datetime)"
      >
        Start
      </BButton>
    </template>
  </BTable>
</template>

<script setup>
const props = defineProps({
  quizzes: Array,
});

const formatDateTime = (value) => {
  if (!value) return "N/A";
  const date = new Date(value * 1000);
  return date;
};

const fields = [
  { key: "title" },
  { key: "subject_title", label: "Subject" },
  { key: "description" },
  { key: "duration", label: "Duration (in mins)" },
  {
    key: "start_datetime",
    label: "Quiz Begins At",
    formatter: formatDateTime,
  },
  { key: "total_questions" },
  { key: "total_marks" },
  {
    key: "actions",
    label: "Actions",
  },
];

const isStartDisabled = (quizStartDatetime) => {
  const quizStartDate = new Date(quizStartDatetime * 1000);
  const currentDate = new Date();
  return currentDate <= quizStartDate;
};
</script>

<template>
  <!-- TITLE -->
  <div class="mb-3">
    <div class="input-group">
      <label for="title" class="input-group-text fw-bold">Title</label>
      <Field name="title" class="form-control"></Field>
    </div>

    <ErrorMessage name="title" class="text-danger mt-1"></ErrorMessage>
  </div>

  <!-- DESCRIPTION -->
  <div class="mb-3">
    <div class="input-group">
      <label for="description" class="input-group-text fw-bold"
        >Description</label
      >
      <Field
        name="description"
        class="form-control"
        as="textarea"
        rows="4"
      ></Field>
    </div>

    <ErrorMessage name="description" class="text-danger mt-1"></ErrorMessage>
  </div>

  <!-- DURATION -->
  <div class="mb-3">
    <div class="input-group">
      <label for="duration" class="input-group-text fw-bold">Duration</label>

      <Field name="duration" class="form-control" type="number"></Field>
    </div>
    <ErrorMessage name="duration" class="text-danger mt-1"></ErrorMessage>
  </div>

  <!-- START DATETIME -->
  <div class="mb-3">
    <div class="input-group">
      <label for="start_datetime" class="input-group-text fw-bold"
        >Start Datetime</label
      >

      <Field
        name="start_datetime"
        class="form-control"
        type="datetime-local"
      ></Field>
    </div>
    <ErrorMessage name="start_datetime" class="text-danger mt-1"></ErrorMessage>
  </div>

  <!-- ATTEMPTS ALLOWED-->
  <div class="mb-3">
    <div class="input-group">
      <label for="duration" class="input-group-text fw-bold"
        >Attempts Allowed</label
      >

      <Field name="attempts_allowed" class="form-control" type="number"></Field>
    </div>
    <ErrorMessage
      name="attempts_allowed"
      class="text-danger mt-1"
    ></ErrorMessage>
  </div>

  <!-- PASSING PERCENTAGE (missing from original template) -->
  <div class="mb-3">
    <div class="input-group">
      <label for="passing_percentage" class="input-group-text fw-bold"
        >Passing Percentage</label
      >
      <Field
        name="passing_percentage"
        class="form-control"
        type="number"
        id="passing_percentage"
      ></Field>
    </div>
    <ErrorMessage
      name="passing_percentage"
      class="text-danger mt-1"
    ></ErrorMessage>
  </div>

  <!-- SUBJECT SELECT -->
  <div class="mb-3">
    <div class="input-group">
      <label for="subject" class="input-group-text fw-bold">Subject</label>
      <Field
        name="subject"
        as="select"
        class="form-select"
        v-model="selectedSubject"
      >
        <option
          v-for="subject in subjectStore.allSubjects"
          :key="subject.id"
          :value="subject.id"
        >
          {{ subject.title }}
        </option>
      </Field>
    </div>
    <ErrorMessage name="subject" class="text-danger mt-1"></ErrorMessage>
  </div>
  <!-- CHAPTER SELECT -->
  <div class="mb-3">
    <div class="input-group">
      <label for="chapter" class="input-group-text fw-bold">Chapter</label>
      <Field name="chapter" as="select" class="form-select">
        <option
          v-for="chapter in chapterStore.allChapters"
          :key="chapter.id"
          :value="chapter.id"
        >
          {{ chapter.title }}
        </option>
      </Field>
    </div>
    <ErrorMessage name="chapter" class="text-danger mt-1"></ErrorMessage>
  </div>
</template>

<script setup>
import { useChapterStore } from "@/stores/dbChapterStore";
import { useSubjectStore } from "@/stores/dbSubjectStore";
import { ErrorMessage, Field } from "vee-validate";
import { onMounted, ref, watch } from "vue";

const subjectStore = useSubjectStore();
const selectedSubject = ref();

onMounted(async () => {
  await subjectStore.fetchSubjects();
});

const chapterStore = useChapterStore();
watch(selectedSubject, (newVal) => {
  if (typeof newVal === "number") {
    chapterStore.fetchChapters(newVal);
  }
});
</script>

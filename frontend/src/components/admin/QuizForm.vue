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
import { ErrorMessage, Field } from "vee-validate";
import { inject, onMounted, watch, watchEffect } from "vue";

const currentSubjectId = inject("currentSubjectId");
const chapterStore = useChapterStore();

watch(currentSubjectId, (newVal) => {
  chapterStore.fetchChapters(newVal);
});
</script>

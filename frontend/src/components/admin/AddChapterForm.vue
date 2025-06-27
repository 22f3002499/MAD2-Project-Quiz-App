<template>
  <Form :validation-schema="addChapterSchema" ref="formRef" class="p-5">
    <div class="mb-3">
      <div class="input-group">
        <label for="title" class="input-group-text fw-bold">Title</label>
        <Field name="title" class="form-control"></Field>
      </div>

      <ErrorMessage name="title" class="text-danger mt-1"></ErrorMessage>
    </div>

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
  </Form>
</template>

<script setup>
import * as yup from "yup";
import { Form, ErrorMessage, Field } from "vee-validate";
import { computed, ref, toRaw } from "vue";
import { useChapterStore } from "@/stores/dbChapterStore";

const chapterStore = useChapterStore();
const formRef = ref();
const addChapterSchema = computed(() =>
  yup.object({
    title: yup.string().required("Title is required"),
    description: yup.string().required("Description is required"),
  }),
);

const submitForm = async (subjectId) => {
  const { valid } = await formRef.value.validate();
  if (valid) {
    await chapterStore.createChapter(subjectId, toRaw(formRef.value.values));
  }

  return valid;
};

const resetForm = () => {
  formRef.value.resetForm();
};

defineExpose({ submitForm, resetForm });
</script>

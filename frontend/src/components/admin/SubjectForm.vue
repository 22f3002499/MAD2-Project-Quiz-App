<template>
  <!-- <Form :validation-schema="subjectSchema" ref="formRef" class="p-5"> -->
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
  <!-- </Form> -->
</template>

<script setup>
import { ErrorMessage, Field } from "vee-validate";
</script>

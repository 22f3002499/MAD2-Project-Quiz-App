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

  <!-- IS CORRECT -->
  <div class="mb-3">
    <div class="input-group">
      <label for="is_correct" class="input-group-text fw-bold"
        >Is Correct</label
      >
      <Field name="is_correct" as="select" class="form-control">
        <option value="">Select...</option>
        <option :value="true">True</option>
        <option :value="false">False</option>
      </Field>
    </div>
    <ErrorMessage name="is_correct" class="text-danger mt-1"></ErrorMessage>
  </div>
  <!-- IMAGE -->
  <div class="mb-3">
    <div class="input-group">
      <label for="_image" class="input-group-text fw-bold">Image</label>
      <Field name="_image" v-slot="{ field, handleChange }">
        <input
          type="file"
          accept="image/*"
          class="form-control"
          @change="(event) => handleImageChange(event, handleChange)"
        />
      </Field>
    </div>
    <ErrorMessage name="_image" class="text-danger mt-1"></ErrorMessage>

    <!-- Image Preview -->
    <div v-if="imagePreview" class="mt-3">
      <div class="card" style="max-width: 300px">
        <BImg
          :src="imagePreview"
          fluid
          class="card-img-top"
          alt="Image preview"
        />
        <div class="card-body p-2">
          <button
            type="button"
            class="btn btn-sm btn-outline-danger"
            @click="removeImage"
          >
            Remove Image
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { Field, ErrorMessage, useFormContext } from "vee-validate";
import { ref } from "vue";

const imagePreview = ref(null);
const { setFieldValue } = useFormContext();

const handleImageChange = (event, handleChange) => {
  const file = event.target.files[0];

  if (file) {
    handleChange(file);

    const reader = new FileReader();
    reader.onload = (e) => {
      imagePreview.value = e.target.result;
    };
    reader.readAsDataURL(file);
  } else {
    imagePreview.value = null;
  }
};

const removeImage = () => {
  // Clear the form field
  setFieldValue("_image", null);
  // Clear the preview
  imagePreview.value = null;
  // Clear the file input
  const fileInput = document.querySelector('input[type="file"]');
  if (fileInput) {
    fileInput.value = "";
  }
};
</script>

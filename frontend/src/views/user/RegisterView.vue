<template>
  <BContainer
    class="d-flex justify-content-center align-items-center"
    style="min-height: 90vh; padding: 20px 0"
  >
    <Form
      :validation-schema="registrationSchema"
      class="card p-5"
      @submit="submit"
      style="width: 500px; max-width: 90vw"
    >
      <div class="mb-3">
        <div class="input-group">
          <label for="email" class="input-group-text fw-bold">Email</label>
          <Field name="email" class="form-control"></Field>
        </div>
        <ErrorMessage name="email" class="text-danger mt-1"></ErrorMessage>
      </div>

      <div class="mb-3">
        <div class="input-group">
          <label for="username" class="input-group-text fw-bold"
            >Username</label
          >
          <Field name="username" class="form-control"></Field>
        </div>
        <ErrorMessage name="username" class="text-danger mt-1"></ErrorMessage>
      </div>

      <div class="mb-3">
        <div class="input-group">
          <label for="password" class="input-group-text fw-bold"
            >Password</label
          >
          <Field name="password" type="password" class="form-control"></Field>
        </div>
        <ErrorMessage name="password" class="text-danger mt-1"></ErrorMessage>
      </div>
      <div class="mb-3">
        <div class="input-group">
          <label for="confirmPassword" class="input-group-text fw-bold"
            >Confirm Password</label
          >
          <Field
            name="confirmPassword"
            type="password"
            class="form-control"
          ></Field>
        </div>
        <ErrorMessage
          name="confirmPassword"
          class="text-danger mt-1"
        ></ErrorMessage>
      </div>
      <div class="mb-3">
        <div class="input-group">
          <label for="dob" class="input-group-text fw-bold">D.O.B.</label>
          <Field name="dob" type="date" class="form-control"></Field>
        </div>
        <ErrorMessage name="dob" class="text-danger mt-1"></ErrorMessage>
      </div>
      <div class="mb-3">
        <label class="form-label fw-bold">Subjects</label>
        <div
          class="border rounded p-2 overflow-y-auto"
          style="max-height: 200px; background-color: #f8f9fa"
        >
          <div
            v-for="subject in subjectStore.allSubjects"
            :key="subject.id"
            class="form-check"
          >
            <Field
              name="subjects"
              type="checkbox"
              :value="subject.id"
              class="form-check-input"
              :id="`subject-${subject.id}`"
            />
            <label
              class="form-check-label"
              :for="`subject-${subject.id}`"
              v-b-tooltip.hover.right="subject.desc"
            >
              {{ subject.title }}
            </label>
          </div>
        </div>
        <ErrorMessage name="subjects" class="text-danger mt-1"></ErrorMessage>
      </div>
      <button type="submit" class="btn btn-primary w-100" :disabled="isLoading">
        {{ isLoading ? "Registering..." : "Register" }}
      </button>
    </Form>
  </BContainer>
</template>

<script setup>
import * as yup from "yup";
import { Form, Field, ErrorMessage } from "vee-validate";
import { useApi } from "@/composables/useApi";
import { useToast } from "@/composables/useToast";
import { useSubjectStore } from "@/stores/dbSubjectStore";
import { onBeforeMount, ref, computed } from "vue";
import { useRouter } from "vue-router";

const subjectStore = useSubjectStore();
onBeforeMount(async () => {
  await subjectStore.fetchSubjects();
});

const getMinAgeDate = (minAge = 14) => {
  const today = new Date();
  const minDate = new Date(
    today.getFullYear() - minAge,
    today.getMonth(),
    today.getDate(),
  );
  return minDate;
};

const registrationSchema = computed(() =>
  yup.object({
    email: yup.string().email().required("Email is required"),
    username: yup.string().required("Username is required"),
    password: yup
      .string()
      .required("Password is required")
      .min(8, "Password must be atleast 8 characters long"),
    confirmPassword: yup
      .string()
      .oneOf([yup.ref("password"), null])
      .required("Please confirm your password"),
    dob: yup.date(getMinAgeDate(14)).nullable(),
    subjects: yup
      .array()
      .of(yup.number().oneOf(subjectStore.allSubjects.map((sub) => sub.id)))
      .min(1, "Atleast one subject must be selected")
      .required("Subjects is a required field"),
  }),
);
const { post, isLoading } = useApi();
const { createErrorToast } = useToast();
const router = useRouter();

async function submit(formData) {
  try {
    await post("/auth/register/", formData);
    router.push({ path: "/login" });
  } catch (err) {
    console.log(err);
    createErrorToast(err?.title || err?.code, err?.message);
  }
}
</script>

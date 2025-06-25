<template>
  <div
    class="d-flex justify-content-center align-items-center"
    style="height: 80vh"
  >
    <Form :validation-schema="schema" class="card p-5" @submit="submit">
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

      <button type="submit" class="btn btn-success w-100" :disabled="isLoading">
        {{ isLoading ? "Logging in..." : "Login" }}
      </button>
    </Form>
  </div>
</template>

<script setup>
import * as yup from "yup";
import { Form, Field, ErrorMessage } from "vee-validate";
import { useAuthStore } from "@/stores/auth";
import { useApi } from "@/composables/useApi";
import { useRouter } from "vue-router";

const schema = yup.object({
  username: yup.string().required(),
  password: yup.string().required(),
});

const auth = useAuthStore();
const { post, isLoading, hasError, error } = useApi();

const router = useRouter();

async function submit(formData) {
  try {
    const response = await post("/auth/login/", formData);
    auth.setToken(response);

    if (auth.userRole === "user") {
      router.push({ path: "/" });
    } else if (auth.userRole === "admin") {
      router.push({ path: "/admin/" });
    }
  } catch (err) {
    console.log(err);
  }
}
</script>

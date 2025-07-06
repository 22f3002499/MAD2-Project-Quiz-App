<template>
  <header>
    <BNavbar variant="secondary-subtle">
      <BNavbarBrand
        ><BButton
          variant="link-dark"
          class="fw-bold fs-3"
          @click="$router.push({ name: 'adminHome' })"
          >Quiz App</BButton
        ></BNavbarBrand
      >

      <BCollapse id="nav-collapse" is-nav>
        <BNavbarNav class="ms-auto fw-bold d-flex align-items-center fs-5">
          <BNavItem class="px-0"
            ><BButton
              variant="link-dark"
              class="fs-5 fw-bold"
              @click="router.push({ name: 'adminSubjects' })"
              >Subjects</BButton
            ></BNavItem
          ><BNavItem class="px-0"
            ><BButton
              variant="link-dark"
              class="fs-5 fw-bold"
              @click="router.push({ name: 'adminQuizzes' })"
              >Quizzes</BButton
            ></BNavItem
          >
          <!-- VERTICAL DIVIDER -->
          <div class="vr mx-2 my-2"></div>
          <BNavItem
            ><BButton variant="danger" class="fs-5 fw-bold" @click="logoutUser"
              >Logout</BButton
            ></BNavItem
          >
        </BNavbarNav>
      </BCollapse>
    </BNavbar>
  </header>
</template>

<script setup>
import { useAuthStore } from "@/stores/auth";
import { useRouter } from "vue-router";

const auth = useAuthStore();
const router = useRouter();

const logoutUser = () => {
  auth.logout();
  router.push({ name: "login" });
};
</script>

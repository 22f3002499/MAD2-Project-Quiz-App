<template>
  <header class="sticky-top shadow-sm">
    <BNavbar variant="secondary-subtle">
      <BNavbarBrand
        ><BButton
          variant="link-dark"
          class="fw-bold fs-3"
          @click="$router.push({ name: 'userHome' })"
          >Quiz App</BButton
        ></BNavbarBrand
      >

      <BCollapse id="nav-collapse" is-nav>
        <BNavbarNav class="ms-auto d-flex align-items-center">
          <BNavItem class="px-0"
            ><BButton
              variant="link-dark"
              class="fw-bold fs-5"
              @click="router.push({ name: 'userStats' })"
              >Stats</BButton
            ></BNavItem
          >

          <BNavItem class="px-0"
            ><BButton
              variant="link-dark"
              class="fs-5 fw-bold"
              @click="router.push({ name: 'userScores' })"
              >Scores</BButton
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

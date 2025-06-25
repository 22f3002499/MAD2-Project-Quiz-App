<template>
  <header>
    <BNavbar variant="secondary-subtle">
      <BNavbarBrand
        tag="h1"
        class="mb-0 fs-3 fw-bold"
        @click="$router.push({ name: 'adminHome' })"
        >Quiz App</BNavbarBrand
      >

      <BCollapse id="nav-collapse" is-nav>
        <BNavbarNav class="ms-auto fw-bold d-flex align-items-center fs-5">
          <BNavItem>Stats</BNavItem>
          <BNavItem @click="router.push({ path: '/scores/' })"
            >totally not scores</BNavItem
          >
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
</script>

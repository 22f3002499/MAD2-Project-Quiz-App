<template>
  <template v-if="auth.isAuthenticated">
    <UserHeader v-if="auth.userRole === 'user'" />
    <AdminHeader v-else-if="auth.userRole === 'admin'" />
  </template>

  <header v-else-if="!auth.isAuthenticated" class="sticky-top">
    <BNavbar variant="secondary-subtle">
      <BNavbarBrand
        tag="h1"
        class="mb-0 fs-3 fw-bold"
        @click="$router.push({ path: '/' })"
        >Quiz App</BNavbarBrand
      >

      <div>
        <BCollapse id="nav-collapse" is-nav>
          <BNavbarNav class="ms-auto fw-bold d-flex align-items-center fs-5">
            <BNavItem>
              <BButton
                variant="success"
                class="fs-5 fw-bold"
                @click="router.push({ name: 'login' })"
                v-if="$route.name === 'register'"
                >Login</BButton
              >
              <BButton
                variant="primary"
                class="fs-5 fw-bold"
                @click="router.push({ name: 'register' })"
                v-else-if="$route.name === 'login'"
                >Register</BButton
              ></BNavItem
            >
          </BNavbarNav>
        </BCollapse>
      </div>
    </BNavbar>
  </header>

  <main>
    <RouterView></RouterView>
    <BToastOrchestrator />
  </main>
</template>

<script setup>
import { RouterView, useRouter } from "vue-router";
import { useAuthStore } from "@/stores/auth";

import UserHeader from "@/components/UserHeader.vue";
import AdminHeader from "@/components/admin/AdminHeader.vue";

const auth = useAuthStore();
const router = useRouter();

const logoutUser = () => {
  auth.logout();
  router.push({ path: "/login/" });
  console.log(localStorage.getItem("token"));
};
</script>

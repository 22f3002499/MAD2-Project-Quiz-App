<template>
  <template v-if="auth.isAuthenticated">
    <UserHeader v-if="auth.userRole === 'user'" />
    <AdminHeader v-else-if="auth.userRole === 'admin'" />
  </template>

  <header v-else-if="!auth.isAuthenticated">
    <BCollapse id="nav-collapse" is-nav>
      <BNavbarNav class="ms-auto fw-bold d-flex align-items-center fs-5">
        <BNavItem>
          <BButton
            variant="success"
            class="fs-5 fw-bold"
            @click="router.push({ path: '/login/' })"
            v-if="$route.path === '/register/'"
            >Login</BButton
          >
          <BButton
            variant="primary"
            class="fs-5 fw-bold"
            @click="router.push({ path: '/register/' })"
            v-else-if="$route.path === '/login/'"
            >Register</BButton
          ></BNavItem
        >
      </BNavbarNav>
    </BCollapse>
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
import AdminHeader from "./components/AdminHeader.vue";

const auth = useAuthStore();
const router = useRouter();

const logoutUser = () => {
  auth.logout();
  router.push({ path: "/login/" });
  console.log(localStorage.getItem("token"));
};
</script>

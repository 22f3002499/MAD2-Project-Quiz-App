<template>
  <BRow cols="3">
    <BCol v-for="chap in store.allChapters" class="mt-4">
      <BCard
        class="h-100"
        footer-bg-variant="light"
        footer-border-variant="white"
        footer-class="text-end"
      >
        <div class="d-flex">
          <div class="fw-bold">{{ chap.title }}</div>
          <BBadge
            class="bg-primary-subtle text-primary ms-auto"
            style="height: fit-content"
            >ID: {{ chap.id }}</BBadge
          >
        </div>
        <p>{{ chap.description }}</p>

        <template #footer>
          <BButton variant="warning" size="sm" class="me-2"
            >Edit Chapter</BButton
          >
          <BButton variant="danger" size="sm" @click="removeChapter(chap.id)"
            >Remove Chapter</BButton
          >
        </template>
      </BCard>
    </BCol>
  </BRow>
</template>

<script setup>
import { useChapterStore } from "@/stores/dbChapterStore";

const store = useChapterStore();

const emit = defineEmits(["refetchChapters"]);

const removeChapter = (chapterId) => {
  store.removeChapter(chapterId);
  emit("refetchChapters");
};
</script>

<template>
  <h2 class="fw-bold text-center mt-5">Subjects</h2>

  <BContainer
    style="max-width: 70vw; max-height: 70vh"
    class="mt-4 overflow-y-scroll"
  >
    <BRow cols="2">
      <BCol v-for="sub in subjectStore.allSubjects" class="mt-4">
        <BCard
          class="h-100"
          footer-bg-variant="light"
          footer-border-variant="white"
          footer-class="text-end"
        >
          <div class="d-flex">
            <div class="fw-bold">{{ sub.title }}</div>
            <BBadge
              class="bg-primary-subtle text-primary ms-auto"
              style="height: fit-content"
              >ID: {{ sub.id }}</BBadge
            >
          </div>
          <p>{{ sub.description }}</p>

          <template #footer>
            <BButton
              variant="primary"
              size="sm"
              class="me-2"
              v-b-modal.view-chapters
              @click="
                () => {
                  chapterStore.fetchChapters(sub.id);
                  currentSubjectId = sub.id;
                }
              "
              >View Chapters</BButton
            >
            <BButton
              variant="success"
              size="sm"
              class="me-2"
              v-b-modal.add-chapter
              @click="currentSubjectId = sub.id"
              >Add Chapter</BButton
            >
            <BButton variant="warning" size="sm" class="me-2"
              >Edit Subject</BButton
            >
            <BButton variant="danger" size="sm" class="me-2"
              >Remove Subject</BButton
            >
          </template>
        </BCard>
      </BCol>
    </BRow>
  </BContainer>

  <BModal
    id="view-chapters"
    scrollable
    title="Chapters"
    ok-only
    size="xl"
    header-variant="primary"
  >
    <ChapterCards />
  </BModal>

  <BModal
    id="add-chapter"
    scrollable
    title="Add Chapter"
    size="lg"
    header-variant="success"
    ref="addChapterModalRef"
  >
    <AddChapterForm ref="addChapterFormRef" />
    <template #footer="{ ok, cancel }">
      <BButton variant="danger" @click="cancel">Cancel</BButton>
      <BButton variant="success" @click="handleAddChapterSubmit"
        >Submit</BButton
      >
    </template>
  </BModal>
</template>

<script setup>
import { onBeforeMount, ref } from "vue";
import { useSubjectStore } from "@/stores/dbSubjectStore";
import { useChapterStore } from "@/stores/dbChapterStore";
import ChapterCards from "@/components/admin/ChapterCards.vue";
import AddChapterForm from "@/components/admin/AddChapterForm.vue";

const subjectStore = useSubjectStore();
const chapterStore = useChapterStore();

onBeforeMount(async () => {
  await subjectStore.fetchSubjects();
});

const addChapterFormRef = ref();
const addChapterModalRef = ref();
const currentSubjectId = ref();

const handleAddChapterSubmit = async () => {
  const formValid = await addChapterFormRef.value.submitForm(
    currentSubjectId.value,
  );
  if (formValid) {
    addChapterModalRef.value.hide();
    addChapterFormRef.value.resetForm();
  }
};
</script>

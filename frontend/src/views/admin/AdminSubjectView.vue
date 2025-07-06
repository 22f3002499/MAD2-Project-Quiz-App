<template>
  <h2 class="fw-bold text-center mt-5">Subjects</h2>

  <BContainer
    style="max-width: 70vw; max-height: 70vh"
    class="mt-4 overflow-y-scroll"
  >
    <SearchBar
      :items="subjectStore.allSubjects"
      @update="handleSearchUpdate"
      class="sticky-top"
    />
    <BRow cols="2">
      <BCol v-for="sub in processedSubjects" class="mt-4">
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
            <!-- VIEW CHAPTER -->
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
            <!-- ADD CHAPTER -->
            <BButton
              variant="success"
              size="sm"
              class="me-2"
              v-b-modal.create-chapter
              @click="currentSubjectId = sub.id"
              >Add Chapter</BButton
            >
            <!-- EDIT SUBJECT -->
            <BButton
              variant="warning"
              size="sm"
              class="me-2"
              v-b-modal.edit-subject
              @click="currentSubjectId = sub.id"
              >Edit Subject</BButton
            >
            <!-- REMOVE SUBJECT -->
            <BButton
              variant="danger"
              size="sm"
              class="me-2"
              @click="
                () => {
                  subjectStore.removeSubject(sub.id);
                  subjectStore.fetchSubjects();
                }
              "
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
    <ChapterCards
      @refetchChapters="chapterStore.fetchChapters(currentSubjectId)"
    />
  </BModal>

  <FormModal
    id="create-chapter"
    title="Create Chapter"
    header-variant="success"
    @submit="handleCreateChapterSubmit"
    :formSchema="chapterSchema"
  >
    <ChapterForm />
  </FormModal>

  <FormModal
    id="edit-subject"
    title="Edit Subject"
    header-variant="warning"
    @submit="handleEditSubjectSubmit"
    :initialData="subjectStore.getSubjectById(currentSubjectId)"
    :formSchema="subjectSchema"
  >
    <SubjectForm />
  </FormModal>
</template>

<script setup>
import { onBeforeMount, ref } from "vue";
import { useSubjectStore } from "@/stores/dbSubjectStore";
import { useChapterStore } from "@/stores/dbChapterStore";

import ChapterCards from "@/components/admin/ChapterCards.vue";
import ChapterForm from "@/components/admin/ChapterForm.vue";
import FormModal from "@/components/FormModal.vue";
import { subjectSchema, chapterSchema } from "@/utils/formSchemas";
import SearchBar from "@/components/SearchBar.vue";

const subjectStore = useSubjectStore();
const chapterStore = useChapterStore();
const currentSubjectId = ref();

onBeforeMount(async () => {
  await subjectStore.fetchSubjects();
});

const handleCreateChapterSubmit = async (formData) => {
  await chapterStore.createChapter(currentSubjectId.value, formData);
};

const handleEditSubjectSubmit = async (formData) => {
  await subjectStore.editSubject(currentSubjectId.value, formData);
};

const processedSubjects = ref([]);
const handleSearchUpdate = (values) => {
  processedSubjects.value = values;
};
</script>

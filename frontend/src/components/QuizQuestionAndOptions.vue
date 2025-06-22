<template>
  <BCol>
    <BContainer style="max-height: 400px" class="overflow-y-scroll">
      <div v-if="store.currentQuestion" class="mt-5">
        <p class="mb-0 fs-5">
          <b>Question ID:</b>{{ store.currentQuestion.id }}
        </p>
        <p>{{ store.currentQuestion.title }}</p>
      </div>
      <div v-if="store.currentQuestion?.description" class="mt-1">
        <BBadge variant="info">Desc</BBadge>
        <span class="ms-2">{{ store.currentQuestion.description }}</span>
      </div>
      <div v-if="store.currentQuestion?.image" class="mt-1">
        <img :src="store.currentQuestion.image" alt="Image not found" />
      </div>
    </BContainer>
  </BCol>
  <BCol class="mt-5">
    <div style="max-height: 400px" class="overflow-y-scroll">
      <BListGroup>
        <BListGroupItem
          class="d-flex justify-content-between align-items-center"
          v-for="(option, index) in store.currentQuestion?.options"
          :key="option.id"
        >
          <BFormCheckbox
            :id="`option-${option.id}`"
            :value="option.id"
            :checked="isOptionSelected(option.id)"
            @change="toggleOption(option.id)"
            class="flex-fill"
            v-if="store.currentQuestion?.type === 'MSQ'"
          >
            <div class="ms-2 me-auto">
              <div class="fw-bold">{{ option.title }}</div>
              {{ option?.description }}
              <img
                v-if="option?.image"
                :src="option?.image"
                alt="No Image found"
              />
            </div>
          </BFormCheckbox>
          <BFormRadio
            :id="`option-${option.id}`"
            :name="`question-${store.currentQuestion?.id}`"
            :value="option.id"
            :model-value="getSelectedRadioValue()"
            @update:model-value="selectRadioOption"
            class="flex-fill"
            v-else-if="store.currentQuestion?.type === 'MCQ'"
          >
            <div class="ms-2 me-auto">
              <div class="fw-bold">{{ option.title }}</div>
              {{ option?.description }}
              <img
                v-if="option?.image"
                :src="option?.image"
                alt="No Image found"
              />
            </div>
          </BFormRadio>
          <BBadge variant="primary" pill>ID {{ option.id }}</BBadge>
        </BListGroupItem>
      </BListGroup>
    </div>
  </BCol>
</template>
<script setup>
import { useStartQuizStore } from "@/stores/startQuizStore";
const store = useStartQuizStore();

function isOptionSelected(optionId) {
  const currentQuestionId = store.currentQuestion?.id;
  if (!currentQuestionId) return false;
  const answers = store.userAnswers[currentQuestionId] || [];
  return answers.includes(optionId);
}

function toggleOption(optionId) {
  const currentQuestionId = store.currentQuestion?.id;
  if (!currentQuestionId) return;
  // Initialize array if it doesn't exist
  if (!store.userAnswers[currentQuestionId]) {
    store.userAnswers[currentQuestionId] = [];
  }
  const answers = store.userAnswers[currentQuestionId];
  const index = answers.indexOf(optionId);
  if (index > -1) {
    store.userAnswers[currentQuestionId] = answers.filter(
      (id) => id !== optionId,
    );
  } else {
    store.userAnswers[currentQuestionId] = [...answers, optionId];
  }
}

function getSelectedRadioValue() {
  const currentQuestionId = store.currentQuestion?.id;
  if (!currentQuestionId) return null;
  const answers = store.userAnswers[currentQuestionId] || [];
  return answers.length > 0 ? answers[0] : null;
}

function selectRadioOption(optionId) {
  const currentQuestionId = store.currentQuestion?.id;
  if (!currentQuestionId) return;
  store.userAnswers[currentQuestionId] = optionId ? [optionId] : [];
}
</script>

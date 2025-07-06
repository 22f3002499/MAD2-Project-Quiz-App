<template>
  <BCard
    v-for="(ques, index) in quizStore.quizQuestionsAndOptions"
    header-bg-variant="light-subtle"
    class="mb-5"
  >
    <template #header>
      <BRow class="my-1">
        <BCol cols="9">
          <!-- QUESTION TITLE AND ID -->
          <BRow>
            <span>
              <BBadge variant="primary" class="me-2 fs-6"
                >ID: {{ ques.id }}</BBadge
              >
              <strong class="fs-5">{{ ques.title }}</strong>
            </span>
          </BRow>

          <!-- QUESTION MARKS AND TYPE BADGES -->
          <BRow class="mt-2">
            <span>
              <BBadge class="bg-success-subtle text-success me-2"
                >{{ ques.marks }} marks</BBadge
              >

              <BBadge class="bg-info-subtle text-info">{{ ques.type }}</BBadge>
            </span>
          </BRow>
        </BCol>

        <!-- QUESTION BUTTONS -->
        <BCol align-self="center">
          <BButtonGroup size="md" class="shadow-sm">
            <BButton
              variant="outline-primary"
              :disabled="props.quizStarted"
              v-b-modal.create-option
              @click="currentQuestion = ques"
              >Add Option</BButton
            >
            <BButton
              variant="outline-warning"
              v-b-modal.edit-question
              @click="currentQuestion = ques"
              :disabled="props.quizStarted"
              >Edit</BButton
            >
            <BButton
              variant="outline-danger"
              :disabled="props.quizStarted"
              @click="
                () => {
                  questionStore.removeQuestion(ques.id);
                  emit('refetchQuestionsAndOptions');
                }
              "
              >Remove</BButton
            >
          </BButtonGroup>
        </BCol>
      </BRow>
    </template>

    <p>{{ ques.description }}</p>
    <BImg
      v-if="ques.image"
      :src="`data:image/png;base64,${ques.image}`"
      fluid
      style="max-height: 500px"
      alt="Could not display question image"
    />

    <BContainer>
      <BRow cols="2" class="g-3">
        <BCol v-for="(opt, index) in ques?.options">
          <BCard
            class="h-100 border border-1 shadow-sm"
            :class="getBorderClass(opt.is_correct)"
          >
            <BRow>
              <BCol cols="8">
                <span>
                  <BBadge
                    class="me-2"
                    :class="getOptionBadgeClass(opt.is_correct)"
                    >{{ index + 1 }}</BBadge
                  >
                  <strong>{{ opt.title }}</strong>
                </span>

                <p>{{ opt.description }}</p>

                <BImg
                  fluid
                  v-if="opt?.image"
                  :src="`data:image/png;base64,${opt?.image}`"
                  alt="Could not load option image"
                />
              </BCol>
              <BCol class="text-end">
                <!-- OPTION BUTTONS -->
                <BDropdown variant="secondary" size="sm">
                  <BDropdownItem
                    :disabled="props.quizStarted"
                    v-b-modal.edit-option
                    @click="currentOption = opt"
                    >Edit</BDropdownItem
                  >
                  <BDropdownItem
                    :disabled="props.quizStarted"
                    @click="
                      {
                        currentOption = opt;
                        optionStore.removeOption(currentOptionId);
                        emit('refetchQuestionsAndOptions');
                      }
                    "
                    >Remove</BDropdownItem
                  >
                </BDropdown>
              </BCol>
            </BRow>
          </BCard>
        </BCol>
      </BRow>
    </BContainer>
  </BCard>

  <FormModal
    id="edit-question"
    title="Edit Question"
    header-variant="warning"
    @submit="handleEditQuestionSubmit"
    :formSchema="questionSchema"
    :initialData="currentQuestion"
  >
    <QuestionForm />
  </FormModal>

  <FormModal
    id="edit-option"
    title="Edit Option"
    header-variant="warning"
    @submit="handleEditOptionSubmit"
    :formSchema="optionSchema"
    :initialData="currentOption"
  >
    <OptionForm />
  </FormModal>

  <FormModal
    id="create-option"
    title="Create Option"
    header-variant="primary"
    @submit="handleCreateOptionSubmit"
    :formSchema="optionSchema"
  >
    <OptionForm />
  </FormModal>
</template>

<script setup>
import { useQuestionStore } from "@/stores/dbQuestionStore";
import { useQuizStore } from "@/stores/dbQuizStore";
import { computed, ref } from "vue";

import FormModal from "../FormModal.vue";
import { questionSchema, optionSchema } from "@/utils/formSchemas";
import { BImg } from "bootstrap-vue-next";
import { useOptionStore } from "@/stores/dbOptionStore";
import QuestionForm from "./QuestionForm.vue";
import OptionForm from "./OptionForm.vue";

const emit = defineEmits(["refetchQuestionsAndOptions"]);

const quizStore = useQuizStore();
const questionStore = useQuestionStore();
const optionStore = useOptionStore();

const props = defineProps({
  quizStarted: {
    type: Boolean,
    required: true,
  },
});

const getBorderClass = (isCorrect) => {
  if (isCorrect) {
    return "border-success";
  }
  return "border-danger";
};

const getOptionBadgeClass = (isCorrect) => {
  if (isCorrect) {
    return "bg-success-subtle text-success";
  }
  return "bg-danger-subtle text-danger";
};

const currentQuestion = ref();
const currentQuestionId = computed(() => currentQuestion.value.id);
const handleEditQuestionSubmit = async (formData) => {
  console.log(
    formData.values(),
    formData.entries(),
    formData.keys(),
    formData.getAll("_image"),
  );
  await questionStore.editQuestion(currentQuestionId.value, formData);
  emit("refetchQuestionsAndOptions");
};

const currentOption = ref();
const currentOptionId = computed(() => currentOption.value.id);
const handleEditOptionSubmit = async (formData) => {
  await optionStore.editOption(currentOptionId.value, formData);
  emit("refetchQuestionsAndOptions");
};

const handleCreateOptionSubmit = async (formData) => {
  await optionStore.createOption(currentQuestionId.value, formData);
  emit("refetchQuestionsAndOptions");
};
</script>

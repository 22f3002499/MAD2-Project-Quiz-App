<template>
  <BModal
    :id="id"
    :title="title"
    :size="size"
    :header-variant="headerVariant"
    scrollable
  >
    <Form ref="formRef" :validation-schema="formSchema">
      <slot />
    </Form>

    <template #footer="{ ok, cancel }">
      <BButton variant="danger" @click="handleCancel"> Cancel </BButton>
      <BButton variant="success" @click="handleSubmit"> Submit </BButton>
    </template>
  </BModal>
</template>

<script setup>
import { useModal } from "bootstrap-vue-next";
import { Form } from "vee-validate";
import { ref, watch } from "vue";

const formRef = ref();
const props = defineProps({
  id: {
    type: String,
    required: true,
  },
  title: {
    type: String,
    required: true,
  },
  headerVariant: {
    type: String,
    default: "primary",
  },
  size: {
    type: String,
    default: "lg",
  },
  formSchema: {
    required: true,
  },
  initialData: {
    type: Object,
    default: {},
  },
});

watch(
  () => props.initialData,
  (newData) => {
    if (newData && Object.keys(newData).length > 0 && formRef.value) {
      formRef.value.setValues(newData);
    }
  },
);

const emit = defineEmits(["submit"]);

const handleSubmit = async () => {
  const { valid } = await formRef.value.validate();
  // ONLY EMIT SUBMIT IF FORM VALID
  if (valid) {
    emit("submit", formRef.value.values);
    formRef.value.resetForm();
    hide();
  }
};

const { hide } = useModal(props.id);
const handleCancel = () => {
  hide();
  formRef.value.resetForm();
};
</script>

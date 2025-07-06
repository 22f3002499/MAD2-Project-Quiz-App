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
      // sets start_datettime if present in the incoming data
      const processedNewData = {
        ...newData,
        start_datetime: newData.start_datetime
          ? new Date(newData.start_datetime * 1000).toISOString().slice(0, 16)
          : null,
        // set chapter to just id
        chapter: newData.chapter?.id ? newData.chapter?.id : null,
      };
      formRef.value.setValues(processedNewData);
    }
  },
);

const emit = defineEmits(["submit"]);

const handleSubmit = async () => {
  const { valid } = await formRef.value.validate();
  if (valid) {
    const schemaKeys = Object.keys(props.formSchema.fields);
    const filteredValues = {};

    for (const key of schemaKeys) {
      if (formRef.value.values[key] !== undefined) {
        filteredValues[key] = formRef.value.values[key];
      }
    }

    if (filteredValues._image && filteredValues._image instanceof File) {
      const formData = new FormData();

      Object.keys(filteredValues).forEach((key) => {
        if (key !== "_image") {
          formData.append(key, filteredValues[key]);
        }
      });

      formData.append("_image", filteredValues._image);

      emit("submit", formData);
      console.log("form Data submitted");
    } else {
      emit("submit", filteredValues);
    }

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

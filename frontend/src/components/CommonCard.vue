<template>
  <BCard
    class="h-100"
    footer-bg-variant="light"
    footer-border-variant="white"
    footer-class="text-end"
  >
    <div class="d-flex">
      <slot name="title-section"></slot>
    </div>

    <slot name="middle-section"></slot>

    <template #footer>
      <slot name="footer-section"></slot>
    </template>
  </BCard>
</template>

<script setup>
const props = defineProps({
  cardClass: {
    type: String,
    default: "h-100",
  },
});
</script>

<template>
  <BCard
    header-border-variant="white"
    header-bg-variant="white"
    footer-border-variant="white"
    footer-bg-variant="white"
  >
    <div class="d-flex align-items-center mb-2">
      <span class="text-secondary"><b>Starts in:</b></span>
      <BBadge class="ms-auto" pill variant="dark">{{ timeRemaining }}</BBadge>
    </div>
    <BProgress
      variant="dark"
      striped
      animated
      :value="progressValue"
      class=""
      height="10px"
    ></BProgress>
    <div class="d-flex align-items-center mt-2">
      <span class="text-secondary">{{ progressText }}</span>
      <BButton variant="outline-secondary" class="ms-auto">
        <i class="bi bi-stopwatch"></i><span> Wait</span>
      </BButton>
    </div>
  </BCard>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from "vue";

const props = defineProps(["quizStartDatetime"]);
const emit = defineEmits(["quiz-ready"]);

const currentTime = ref(new Date());
let intervalId = null;

onMounted(() => {
  intervalId = setInterval(() => {
    currentTime.value = new Date();
  }, 1000);
});

onUnmounted(() => {
  if (intervalId) {
    clearInterval(intervalId);
  }
});

const timeRemaining = computed(() => {
  const quizDatetime = new Date(props.quizStartDatetime * 1000);
  const timeDiff = quizDatetime - currentTime.value;

  if (timeDiff <= 0) {
    return "Started";
  }

  const numDays = Math.floor(timeDiff / (1000 * 60 * 60 * 24));
  const numHours = Math.floor((timeDiff / (1000 * 60 * 60)) % 24);
  const numMins = Math.floor((timeDiff / (1000 * 60)) % 60);
  const numSecs = Math.floor((timeDiff / 1000) % 60);

  const parts = [];
  if (numDays > 0) parts.push(`${numDays}d`);
  if (numHours > 0) parts.push(`${numHours}h`);
  if (numMins > 0) parts.push(`${numMins}m`);
  if (numSecs > 0) parts.push(`${numSecs}s`);

  return parts.join(" ");
});

const progressValue = computed(() => {
  const quizDatetime = new Date(props.quizStartDatetime * 1000);
  const timeDiff = quizDatetime - currentTime.value;

  if (timeDiff <= 0) {
    return 0;
  }

  const totalCountdownPeriod = 7 * 24 * 60 * 60 * 1000; // 7 days in milliseconds
  const progress = Math.max(
    0,
    Math.min(100, (timeDiff / totalCountdownPeriod) * 100),
  );

  return Math.round(progress);
});

const progressText = computed(() => {
  if (progressValue.value === 0) return "Ready to Start!";
  if (progressValue.value > 95) return "Just Announced";
  if (progressValue.value > 75) return "Getting Ready";
  if (progressValue.value > 50) return "Preparing...";
  if (progressValue.value > 25) return "Almost There";
  return "Preparing...";
});

// EMIT EVENT WHEN PROGRESS VALUE HITS 0 TO SHOW QUIZ BUTTON
watch(progressValue, (newValue) => {
  if (newValue === 0) {
    emit("quiz-ready");
  }
});
</script>

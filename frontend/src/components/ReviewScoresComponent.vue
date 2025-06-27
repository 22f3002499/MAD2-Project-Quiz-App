<template>
  <BListGroup flush>
    <BListGroupItem v-for="ques in store.userAnswers" class="mb-5 ps-3 pe-2">
      <BContainer fluid>
        <BRow>
          <BCol>
            <div class="d-flex justify-content-between align-items-center">
              <h5>{{ ques.title }}</h5>
              <div>
                <BBadge pill class="me-2 bg-info-subtle text-info"
                  >ID: {{ ques.id }}</BBadge
                >
                <BBadge pill variant="primary" class="me-2"
                  >Marks: {{ ques.marks }}</BBadge
                >
                <BBadge pill variant="warning">Type: {{ ques.type }}</BBadge>
              </div>
            </div>
            <p v-if="ques.description">{{ ques.description }}</p>
            <img :src="ques.image" alt="No image found" v-if="ques.image" />
          </BCol>
        </BRow>

        <BRow class="mt-2 g-2" cols="2">
          <BCol v-for="opt in ques.options">
            <BCard
              :border-variant="opt.is_correct ? 'success' : 'danger'"
              class="h-100"
            >
              <div class="d-flex">
                <div class="fw-bold">{{ opt.title }}</div>
                <BBadge
                  pill
                  class="ms-auto"
                  :class="getBadgeClass(opt.is_correct)"
                  >ID: {{ opt.id }}</BBadge
                >
              </div>

              <p v-if="opt.description">{{ opt.description }}</p>
              <img :src="opt.image" alt="No image found" v-if="opt.image" />
            </BCard>
          </BCol>
        </BRow>

        <BRow class="mt-4 mb-3">
          <BCard bg-variant="primary-subtle">
            <span class="text-primary fw-bold me-2">User Answers:</span>
            <span
              ><BBadge
                v-for="optId in ques.user_selected_options"
                pill
                variant="primary"
                class="me-1"
                >ID: {{ optId }}</BBadge
              ></span
            >
          </BCard>
        </BRow>
      </BContainer>
    </BListGroupItem>
  </BListGroup>
</template>

<script setup>
import { useScoresStore } from "@/stores/scoresStore";

const store = useScoresStore();

const getBadgeClass = (bool) => {
  if (bool) return "bg-success-subtle text-success";
  else return "bg-danger-subtle text-danger";
};
</script>

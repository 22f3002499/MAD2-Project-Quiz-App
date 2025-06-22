<template>
  <BListGroup>
    <BListGroupItem v-for="ques in store.userAnswers" class="mb-5">
      <BContainer fluid>
        <BRow>
          <BCol>
            <div class="d-flex justify-content-between align-items-center">
              <h5>{{ ques.title }}</h5>
              <div>
                <BBadge pill variant="info" class="me-2"
                  >ID: {{ ques.id }}</BBadge
                >
                <BBadge pill variant="primary">Marks: {{ ques.marks }}</BBadge>
              </div>
            </div>
            <p>{{ ques.description }}</p>
            <img :src="ques.image" alt="No image found" v-if="ques.image" />
          </BCol>
        </BRow>

        <BRow class="mt-3">
          <BListGroup>
            <BListGroupItem v-for="opt in ques.options">
              <div class="d-flex justify-content-between align-items-center">
                <div class="fw-bold">{{ opt.title }}</div>
                <BBadge pill :variant="opt.is_correct ? 'success' : 'secondary'"
                  >ID: {{ opt.id }}</BBadge
                >
              </div>
              <p>{{ opt.description }}</p>
              <img :src="opt.image" alt="No image found" v-if="opt.image" />
            </BListGroupItem>
          </BListGroup>
        </BRow>

        <BRow class="mt-3">
          <p>
            User Answers:
            <BBadge
              class="me-2"
              variant="dark"
              pill
              v-for="optId in ques.user_selected_options"
              >ID: {{ optId }}</BBadge
            >
          </p>
        </BRow>
      </BContainer>
    </BListGroupItem>
  </BListGroup>
</template>

<script setup>
import { useScoresStore } from "@/stores/scoresStore";

const store = useScoresStore();
</script>

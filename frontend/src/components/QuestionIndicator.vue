<template>
  <BContainer class="px-0 mx-3 my-4">
    <BRow cols="2" :no-gutters="true" class="px-4">
      <BCol class="d-flex align-items-center">
        <BButton variant="danger" class="text-center rounded p-3 px-4"
          >2</BButton
        >
        <span class="ms-2">Unanswered</span>
      </BCol>
      <BCol class="d-flex align-items-center">
        <BButton variant="success" class="text-center rounded p-3 px-4"
          >7</BButton
        >
        <span class="ms-2">Answered</span>
      </BCol>
      <BCol class="d-flex align-items-center mt-3">
        <BButton variant="outline-dark" class="text-center rounded p-3 px-4"
          >5</BButton
        >
        <span class="ms-2">Not Visited</span>
      </BCol>
    </BRow>
  </BContainer>
</template>

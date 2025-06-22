import { useApi } from "@/composables/useApi";
import { defineStore } from "pinia";
import { readonly, ref } from "vue";

export const useScoresStore = defineStore('score', () => {
  const { get, post } = useApi();

  const scores = ref([]);
  const _userAnswers = ref([]); // Internal mutable ref

  async function getScores() {
    try {
      const response = await get('/user/scores/');
      scores.value = response;
    } catch (err) {
      // handle error
    }
  }

  async function getUserAnswers(quizAttemptId) {
    try {
      const response = await get(`/user/review-answers/${quizAttemptId}/`);
      _userAnswers.value = response;
    } catch (err) {
      // handle error
    }
  }

  async function downloadUserAnswers(quizAttemptId){
    try{
      const response = await get(`/user/review-answers/${quizAttemptId}/?download=true`,{
        responseType:'blob'
      })

      const blob = new Blob([response] , {type:"application/json"})

      const link = document.createElement("a")
      link.href = URL.createObjectURL(blob)
      link.download = `userAnswers-${quizAttemptId}.json`

      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
    } catch (err){
      // handle error
    }
  }

  const userAnswers = readonly(_userAnswers);

  return { scores, userAnswers, getScores, getUserAnswers ,downloadUserAnswers };
});

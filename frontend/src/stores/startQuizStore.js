import { computed, ref, toRaw, watch } from "vue";
import { defineStore } from "pinia";
import { useApi } from "@/composables/useApi";

export const useStartQuizStore = defineStore('startQuizStore' , ()=>{

  const USER_ANSWERS_STORAGE_KEY = 'userAnswers'
  const VISITED_QUESTIONS_STORAGE_KEY = 'visistedQuestions'

  const {get,post} = useApi()
  const questionAndOptions = ref([])
  const currentQuestion = ref(null)
  const quizDuration = ref(null)

  // store key value pairs of question id and option id
  // {
  //    ques_id:[opt_id , opt_id , opt_id]
  // }
  const userAnswers = ref(JSON.parse(localStorage.getItem(USER_ANSWERS_STORAGE_KEY)) || {});

  //store the visisted question ids in an array
  const visitedQuestions = ref(JSON.parse(localStorage.getItem(VISITED_QUESTIONS_STORAGE_KEY)) || [])

  
  const startQuiz = async (quizId) => {
  /*
  The response recieved is a list of 2 items
  the first item is a list of objects which question and option details
  {
    id,
    title,
    description,
    image,
    options: [{
      id,
      title,
      image,
      description
      },
    ]
  }

  the second item is quiz duration
  */
    try{      
      const response = await get(`/user/start-quiz/${quizId}/`)
      questionAndOptions.value = response[0]
      quizDuration.value = response[1]["quiz_duration"]
    }catch (err){
      // display error
    }
  }

  function getQuestionById(quesId){
    return questionAndOptions.value.find((item )=> item.id === quesId)
  }


  watch(userAnswers , (newVal) => {
    localStorage.setItem(USER_ANSWERS_STORAGE_KEY , JSON.stringify(toRaw(newVal)))
  } , {deep:true})

  watch(visitedQuestions , (newVal) => {
    localStorage.setItem(VISITED_QUESTIONS_STORAGE_KEY, JSON.stringify(toRaw(newVal)))
  })


  function clearStoredAnswers(){
    localStorage.removeItem(USER_ANSWERS_STORAGE_KEY)
    userAnswers.value = {}
  }

  function clearVisitedQuestions(){
    localStorage.removeItem(VISITED_QUESTIONS_STORAGE_KEY)
    visitedQuestions.value = []
  }


  async function submitQuiz(quizId){
    try{      
      const response = await post(`/user/submit-quiz/${quizId}/` , toRaw(JSON.parse(localStorage.getItem(USER_ANSWERS_STORAGE_KEY))))
      clearStoredAnswers()
      clearVisitedQuestions()
    } catch (err){
      // display error
    }
  }

  return {questionAndOptions , currentQuestion,userAnswers, visitedQuestions,quizDuration, startQuiz , getQuestionById , submitQuiz}
})

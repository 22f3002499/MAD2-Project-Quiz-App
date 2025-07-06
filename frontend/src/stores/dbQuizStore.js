import { useApi } from "@/composables/useApi";
import { useToast } from "@/composables/useToast";
import { defineStore } from "pinia";
import { ref } from "vue"; 

export const useQuizStore = defineStore('quizStore' , () => {
  const {get ,post , put} = useApi()
  const delay = (ms) => new Promise(resolve => setTimeout(resolve , ms))

  const userQuizzes = ref([])
  const allQuizzes = ref([])

  const toast = useToast()

  
  const getUserQuizzes = async () =>{
    try{
      const response = await get('/user/quiz/')
      userQuizzes.value = response
    } catch (err){
      // await delay(2000)
      // await getUserQuizzes()
    }    
  }

  const fetchAllQuizzes = async () => {
    try{
      const response = await get('/admin/quizzes/')
      allQuizzes.value = response
    } catch (err){
      //
    }
  }


  const addQuiz = async (quizData) => {
    try{
      const response = await post('/admin/create/quiz/' , quizData)
      await getUserQuizzes()
    } catch (err){
      // display toast notification if error
      
    }
  }

  const editQuiz = async (quizId , quizData) =>{
    try{
      const response = await put(`/admin/edit/quiz/${quizId}/` , quizData)
      await fetchAllQuizzes()
    } catch (err){
      // display toast notification if error 
    }
  }

  const removeQuiz = async (quizId) =>{
    try{
      const response = await put(`/admin/edit/quiz/${quizId}/` , {"is_deleted" : true})
      toast.createSuccessToast(response?.message , "")
    } catch (error){
      toast.createErrorToast(error.code , JSON.stringify(error?.response?.data) || error?.message)
    }
  }

  
  const getQuizById = (quizId) => {
    return allQuizzes.value.find((quiz) => quiz.id === quizId) || {}
  }

  const quizQuestionsAndOptions = ref(null)
  async function getQuizQuestionsAndOptions(quizId) {
    try{
      const response = await get(`/admin/quiz/questions-and-options/${quizId}/`)
      quizQuestionsAndOptions.value = response
    } catch (error){
      
    }
  }
  

  return {userQuizzes ,allQuizzes,  addQuiz , editQuiz ,  removeQuiz ,  getUserQuizzes , fetchAllQuizzes , getQuizById , quizQuestionsAndOptions , getQuizQuestionsAndOptions}
})

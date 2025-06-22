import { useApi } from "@/composables/useApi";
import { defineStore } from "pinia";
import { ref } from "vue"; 

export const useQuizStore = defineStore('quizStore' , () => {
  const {get ,post} = useApi()
  const delay = (ms) => new Promise(resolve => setTimeout(resolve , ms))

  const userQuizzes = ref([])
  const sortedQuizzes = ref([])

  
  const getUserQuizzes = async () =>{
    try{
      const response = await get('/user/quiz/')
      userQuizzes.value = response
    } catch (err){
      // await delay(2000)
      // await getUserQuizzes()
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

  const editQuiz = async (quizData) =>{
    try{
      const response = await post('/admin/edit/quiz/' , quizData)
      await getUserQuizzes()
    } catch (err){
      // display toast notification if error 
    }
  }

  const deleteQuiz = async (quizId) =>{
    try{
      const response = await post(`/admin/edit/quiz/${quizId}` , {"is_deleted" : true})
      await getUserQuizzes()
    } catch (err){
      // display toast notification if error 
    }
  }
  
  const sortQuizzes = (key) => {
    if (key.includes('time') || key.includes('date')){
      sortedQuizzes.value = [...userQuizzes.value].sort((a , b) => {
        return new Date(a.key) - new Date(b.key)
      })
    }

    else if (key.includes('id') || key.includes('total') || key.includes('duration')){
      sortedQuizzes.value = [...userQuizzes.value].sort((a,b) => {
        return new Number(a.key) - new Number(b.key)
      })
    }

    else {
      sortedQuizzes.value = [...userQuizzes.value].sort()
    }
  }


  return {userQuizzes , sortedQuizzes , addQuiz , editQuiz , deleteQuiz , sortQuizzes , getUserQuizzes}
})

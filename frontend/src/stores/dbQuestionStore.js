import { useApi } from "@/composables/useApi";
import { useToast } from "@/composables/useToast";
import { defineStore } from "pinia";

export const useQuestionStore = defineStore('questionStore' , () => {

  const {get , post , put} = useApi()
  const toast = useToast()

  async function createQuestion(quizId,formData){
    let requestHeaders = {'Content-Type' : 'application/json' , Accept:'application/json'}

    if (formData instanceof FormData){      
      for (const key of formData.keys()){
        if (key === "_image"){
          requestHeaders = {'Content-Type' : 'multipart/form-data' , Accept:'application/json'}
        }
      }
    }

    try{
      const response = await post(`/admin/create/question/?quiz_id=${quizId}` , formData , {
        headers:requestHeaders
      })
    } catch (error){
      
    }
  }

  

  async function removeQuestion(questionId){
    try{
      const response = await put(`/admin/edit/question/${questionId}/` , {"is_deleted": true})
    } catch (error){
      
    }
  }

  async function editQuestion(questionId , formData){
    let requestHeaders = {'Content-Type' : 'application/json' , Accept:'application/json'}

    if (formData instanceof FormData){      
      for (const key of formData.keys()){
        if (key === "_image"){
          requestHeaders = {'Content-Type' : 'multipart/form-data' , Accept:'application/json'}
        }
      }
    }

    try{
      const response = await put(`/admin/edit/question/${questionId}/` , formData , {
        headers:requestHeaders
      })
    } catch (error){
      
    }
  }

  return {removeQuestion ,editQuestion ,createQuestion}
})

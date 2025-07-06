import { useApi } from "@/composables/useApi";
import { useToast } from "@/composables/useToast";
import { defineStore } from "pinia";

export const useQuestionStore = defineStore('questionStore' , () => {

  const {get , post , put} = useApi()
  const toast = useToast()

  async function removeQuestion(questionId){
    try{
      const response = await put(`/admin/edit/question/${questionId}/` , {"is_deleted": true})
    } catch (error){
      
    }
  }

  async function editQuestion(questionId , formData){
    let requestHeaders = {'Content-Type' : 'application/json' , Accept:'application/json'}

    for (const key of formData.keys()){
      if (key === "_image"){
        requestHeaders = {'Content-Type' : 'multipart/form-data' , Accept:'application/json'}
      }
    }

    try{
      const response = await put(`/admin/edit/question/${questionId}/` , formData , {
        headers:requestHeaders
      })
    } catch (error){
      
    }
  }

  return {removeQuestion ,editQuestion}
})

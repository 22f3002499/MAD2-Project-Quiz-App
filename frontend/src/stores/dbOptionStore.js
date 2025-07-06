
import { useApi } from "@/composables/useApi";
import { useToast } from "@/composables/useToast";
import { defineStore } from "pinia";

export const useOptionStore = defineStore('OptionStore' , () => {

  const {get , post , put} = useApi()
  const toast = useToast()

  async function createOption(questionId , formData){
    let requestHeaders = {'Content-Type' : 'application/json' , Accept:'application/json'}
    
    if (formData instanceof FormData){
      for (const key of formData.keys()){
        if (key === "_image"){
          requestHeaders = {'Content-Type' : 'multipart/form-data' , Accept:'application/json'}
        }
      }
    }    
    
    try{
      const response = await post(`/admin/create/option/?question_id=${questionId}` , formData , {headers:requestHeaders})
    } catch (error){
      
    }
  }

  async function removeOption(optionId){
    try{
      const response = await put(`/admin/edit/option/${optionId}/` , {"is_deleted": true})
    } catch (error){
      
    }
  }

  async function editOption(optionId , formData){
    let requestHeaders = {'Content-Type' : 'application/json' , Accept:'application/json'}
    
    if (formData instanceof FormData){
      for (const key of formData.keys()){
        if (key === "_image"){
          requestHeaders = {'Content-Type' : 'multipart/form-data' , Accept:'application/json'}
        }
      }
    }
    
    try{
      const response = await put(`/admin/edit/option/${optionId}/` , formData , {
        headers:requestHeaders
      })
    } catch (error){
      
    }
  }

  return {removeOption ,editOption ,createOption}
})

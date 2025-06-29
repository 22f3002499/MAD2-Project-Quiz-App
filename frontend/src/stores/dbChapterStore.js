import { defineStore } from "pinia"
import { useApi } from "@/composables/useApi";
import { useToast } from "@/composables/useToast";

import { ref } from "vue"; 

export const useChapterStore = defineStore('chapterStore' , () => {
  const {get , post , put} = useApi()
  const toast = useToast()

  const allChapters = ref([])

  async function fetchChapters(subjectId){
    try{
      const response = await get(`/admin/chapters/${subjectId}/`)
      allChapters.value = response
    } catch (error){
      toast.createErrorToast(error.code , JSON.stringify(error?.response?.data) || error?.message)
    }
  }

  async function createChapter(subjectId , formData){
    try{
      const response = await post(`/admin/create/chapter/?subject_id=${subjectId}` , formData)
      toast.createSuccessToast(response , "")
    } catch (error){
      toast.createErrorToast(error.code , JSON.stringify(error?.response?.data) || error?.message)
    }
  }

  async function removeChapter(chapterId){
    try{
      const response = await put(`/admin/edit/chapter/${chapterId}/` , {"is_deleted" : true})
      toast.createSuccessToast(response?.message , "")
    } catch (error){
      toast.createErrorToast(error.code , JSON.stringify(error?.response?.data) || error?.message)
    }
  }

  async function editChapter(chapterId , newData){
    try{
      const response = await put(`/admin/edit/chapter/${chapterId}/` , newData)
    } catch (error){
      
      toast.createErrorToast(error.code , JSON.stringify(error?.response?.data) || error?.message)
    }
  }

  function getChapterById(chapterId){
    return allChapters.value.find((chap) => chap.id === chapterId)
  }

  return {allChapters , fetchChapters , createChapter ,removeChapter , editChapter , getChapterById}

  
  
})

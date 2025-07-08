import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { useApi } from '@/composables/useApi'
import { useToast } from '@/composables/useToast'

// isLoading can be added from useApi composable
// but am not sure how well it will work
export const useSubjectStore = defineStore('subjectStore', () => {
  const delay = (ms) => new Promise(resolve => setTimeout(resolve , ms))
  const {get  , post  , put} = useApi()
  
  const subjects = ref([])
  const allSubjects = computed(() => subjects.value)
  const toast = useToast()

  const fetchSubjects = async () => {
    try{
      // get all the {id , title} subject pairse from the route with no auth
      const response = await get('/other/subject/')
      subjects.value = response
    } catch (err){
      console.log(err || response.data?.message || response.message || response)
      await delay(2000)
      await fetchSubjects()
    }
  }

  const createSubject = async (formData) =>{
    try{
      const response = await post('/admin/create/subject/' , formData)
    }catch (error){
      toast.createErrorToast(error.code , JSON.stringify(error?.response?.data) || error?.message)
    }
  }
  
  const editSubject = async (subjectId , newData) => {
    try{
      const response = await put(`/admin/edit/subject/${subjectId}/` , newData)
      await fetchSubjects()
    } catch (error){
      toast.createErrorToast(error.code , JSON.stringify(error?.response?.data) || error?.message)
    }
  }

  const removeSubject = async (subjectId) => {
    try{
      const response = await put(`/admin/edit/subject/${subjectId}/` , {"is_deleted" : true})
    } catch (err){
      toast.createErrorToast(error.code , JSON.stringify(error?.response?.data) || error?.message)
    }
  }

  const getSubjectById = (subjectId) => {
    return subjects.value.find((sub) => sub.id === subjectId)
  }



  return {allSubjects, fetchSubjects , createSubject , removeSubject ,editSubject , getSubjectById}
})




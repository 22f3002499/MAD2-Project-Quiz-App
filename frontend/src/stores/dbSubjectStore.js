import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { useApi } from '@/composables/useApi'

// isLoading can be added from useApi composable
// but am not sure how well it will work
export const useSubjectStore = defineStore('subjectStore', () => {
  const delay = (ms) => new Promise(resolve => setTimeout(resolve , ms))
  const {get  , post } = useApi()
  
  const subjects = ref([])
  const allSubjects = computed(() => subjects.value)

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

  const addSubject = async (subjectDetails) =>{
    try{
      const response = await post('/admin/create/subject/' , subjectDetails)
      await fetchSubjects()
    }catch (err){
      console.log(err || response.data?.message || response.message || response)
    }
  }
  const editSubject = async (subjectDetails) =>{
    try{
      const response = await post('/admin/edit/subject/' , subjectDetails)
      await fetchSubjects()
    }catch (err){
      console.log(err || response.data?.message || response.message || response)
    }
  }



  return {allSubjects, fetchSubjects , addSubject , editSubject}
})




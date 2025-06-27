import { useApi } from "@/composables/useApi"
import { useToast } from "@/composables/useToast";
import { defineStore } from "pinia";
import { ref } from "vue";

export const useUserStatsStore = defineStore('userStats' , () => {
  const {get , post} = useApi()
  const stats = ref({})

  const toast = useToast()

  async function getStats(){
    try{
      const response = await get('/user/stats/')
      stats.value = response
    } catch (error){
      toast.createErrorToast(error.code , JSON.stringify(error?.response?.data) || error?.message)
    }
  }

  return {stats ,getStats}
})

import { useApi } from "@/composables/useApi";
import { defineStore } from "pinia";

export const useUserStore = defineStore('userStore' , () => {
  const {get , post , put} = useApi()

  async function fetchUsers(){
    try{
      const response = get('/admin/users/')
    } catch (error){
      
    }
  }

  async function banUser(userId){
    try{
      const response = put(`/admin/edit/user/${userId}/` , {'is_banned' : true})
    } catch (error){
      
    }
  }
  
  async function removeUser(userId){
    try{
      const response = put(`/admin/edit/user/${userId}/` , {'is_deleted' : true})
    } catch (error){
      
    }
  }
})

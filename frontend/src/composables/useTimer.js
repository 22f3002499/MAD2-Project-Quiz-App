import { computed, ref } from "vue";

// its assumed the duration will be passed as mins
export function useTimer(duration = 0 , onTimerEnd = null){
  const TIME_LEFT_STORAGE_KEY = 'timeLeft'
  
  const timerStarted = ref(false)
  const timeLeft = ref(localStorage.getItem(TIME_LEFT_STORAGE_KEY) || duration * 60)
  const formattedTime = computed(() => {
    const mins = Math.floor(timeLeft.value / 60)
    const secs = timeLeft.value % 60
    return `${mins.toString().padStart(2, "0")}:${secs.toString().padStart(2, "0")}`;
  })

  let intervalId = null
  function startTimer(){
    if (!timerStarted.value){
      timerStarted.value = true

      intervalId = setInterval(()=>{
        if (timeLeft.value > 0){
          timeLeft.value--
          localStorage.setItem(TIME_LEFT_STORAGE_KEY , timeLeft.value)
        } else {
          stopTimer()
          if (onTimerEnd && typeof onTimerEnd === "function"){
            onTimerEnd()
          }
        }
      },1000)
    }
  }

  function stopTimer(){
    timeLeft.value = 0
    clearInterval(intervalId)
    timerStarted.value = false
    localStorage.removeItem(TIME_LEFT_STORAGE_KEY)
  }

  return {formattedTime , startTimer , stopTimer}
}

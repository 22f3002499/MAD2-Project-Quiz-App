import { useToastController } from "bootstrap-vue-next";
import { ref , computed  , h} from "vue";

export function useToast(){
  const {create} = useToastController()
  
  const createToast = (title , content , variant,iconString) => {

    create({
      variant: variant,
      position: "bottom-end",
      modelValue: 7000,
      slots: {
        title: ({ hide }) => [
          h('div', { class: "fw-bold" }, [
            h('i', { class: `bi bi-${iconString} me-2` }),
            title
          ])
        ],
        default: () => h('pre', { 
          class: "mb-0 text-wrap text-break lh-base"
        }, content)
      }
    }, { resolveOnHide: true });
  }

  const createErrorToast = (title,content) => {
    createToast(title , content , "danger" , "exclamation-circle-fill")
  }
  const createSuccessToast = (title,content) => {
    createToast(title , content , "success" , "check-circle-fill")
  }
  const createInfoToast = (title,content) => {
    createToast(title , content , "primary" , "info-circle-fill")
  }

  return {createErrorToast ,createSuccessToast, createInfoToast}
}

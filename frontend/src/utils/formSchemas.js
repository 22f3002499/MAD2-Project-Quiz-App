import { computed } from "vue";
import * as yup from "yup";

export const chapterSchema = computed(() =>
  yup.object({
    title: yup.string().required("Title is required"),
    description: yup.string().required("Description is required"),
  }),
);

export const subjectSchema = computed(() =>
  yup.object({
    title: yup.string().required("Title is required"),
    description: yup.string().required("Description is required"),
  }),
);

export const quizSchema = computed(() => {
  
  return yup.object({
    title: yup.string().required("Title is required"),
    description: yup.string().required("Description is required"),
    duration:yup.number().min(10).required("Duration is required"),
    start_datetime:yup.date().min(new Date()).required("Date is required"),
    passing_percentage:yup.number().min(20).max(80).required("Passing Percentage is required"),
    attempts_allowed:yup.number().min(1).required("Number of Attempts Allowed is required"),
    chapter:yup.number().required("Chapter is required"),
  })
})

export const questionSchema = computed(() => {

  return yup.object({
    title: yup.string().required("Title is required"),
    description: yup.string().optional("Description is optional"),
    marks:yup.number().min(1),    
    _image: yup
    .mixed()
    .nullable()
    .test('fileSize', 'File size must be less than 5MB', (value) => {
      if (!value || !value[0]) return true; // Allow empty for optional fields
      return value[0].size <= 1 * 1024 * 1024; // 5MB limit
    })
    .test('fileType', 'Only image files are allowed', (value) => {
      if (!value || !value[0]) return true;
      return ['image/jpeg', 'image/png', 'image/gif', 'image/webp'].includes(value[0].type);
    }),
  })
  
})

export const optionSchema = computed(() => {

  return yup.object({
    title: yup.string().required("Title is required"),
    description: yup.string().optional("Description is optional"),
    is_correct:yup.boolean().required("Option is_correct is required"),
    _image: yup
    .mixed()
    .nullable()
    .test('fileSize', 'File size must be less than 5MB', (value) => {
      if (!value || !value[0]) return true; // Allow empty for optional fields
      return value[0].size <= 1 * 1024 * 1024; // 5MB limit
    })
    .test('fileType', 'Only image files are allowed', (value) => {
      if (!value || !value[0]) return true;
      return ['image/jpeg', 'image/png', 'image/gif', 'image/webp'].includes(value[0].type);
    }),
  })
})


import Vue from 'vue'
import VueRouter from 'vue-router'
import Dashboard from "@/views/Dashboard";
import ReadingBase from "@/components/Subcomponents/DesignExam/reading/ReadingBase";
import RegisterLogin from "@/views/RegisterLogin";
import AddReading from "@/components/Subcomponents/DesignExam/reading/AddReading";
import EditReading from "@/components/Subcomponents/DesignExam/reading/EditReading";
import ReadingQuestions from "@/components/Subcomponents/DesignExam/reading/ReadingQuestions";
import AddReadingQuestion from "@/components/Subcomponents/DesignExam/reading/AddReadingQuestion";

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Dashboard
  },
    {
    path: '/reading',
    name: 'Reading',
    component: ReadingBase
  },
     {
    path: '/add_reading',
    name: 'AddReading',
    component: AddReading
  },
  {
    path: '/edit_reading',
    name: 'EditReading',
    component: EditReading
  },
    {
    path: '/questions_reading',
    name: 'QuestionsReading',
    component: ReadingQuestions
  },
      {
    path: '/add_reading_question',
    name: 'AddReadingQuestion',
    component: AddReadingQuestion
  },
      {
    path: '/login',
    name: 'Login',
    component: RegisterLogin
  },
]

const router = new VueRouter({
  routes
})

export default router

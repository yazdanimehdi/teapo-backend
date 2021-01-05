import Vue from 'vue'
import VueRouter from 'vue-router'
import Dashboard from "@/views/Dashboard";
import RegisterLogin from "@/views/RegisterLogin";

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
        component: () => import('@/components/Subcomponents/DesignExam/reading/ReadingBase')
    },
    {
        path: '/add_reading',
        name: 'AddReading',
        component: () => import('@/components/Subcomponents/DesignExam/reading/AddReading')
    },
    {
        path: '/edit_reading',
        name: 'EditReading',
        component: () => import('@/components/Subcomponents/DesignExam/reading/EditReading')
    },
    {
        path: '/questions_reading',
        name: 'QuestionsReading',
        component: () => import('@/components/Subcomponents/DesignExam/reading/ReadingQuestions')
    },
    {
        path: '/add_reading_question',
        name: 'AddReadingQuestion',
        component: () => import('@/components/Subcomponents/DesignExam/reading/AddReadingQuestion')
    },
    {
        path: '/listening',
        name: 'Listening',
        component: () => import('@/components/Subcomponents/DesignExam/listening/ListeningBase')
    },
    {
        path: '/add_listening',
        name: 'AddListening',
        component: () => import('@/components/Subcomponents/DesignExam/listening/AddListening')
    },
    {
        path: '/edit_listening',
        name: 'EditListening',
        component: () => import('@/components/Subcomponents/DesignExam/listening/EditListening')
    },
    {
        path: '/questions_listening',
        name: 'QuestionsListening',
        component: () => import('@/components/Subcomponents/DesignExam/listening/ListeningQuestions')
    },
     {
        path: '/add_listening_question',
        name: 'AddListeningQuestion',
        component: () => import('@/components/Subcomponents/DesignExam/listening/AddListeningQuestion')
    },
    {
        path: '/speaking',
        name: 'Speaking',
        component: () => import('@/components/Subcomponents/DesignExam/speaking/SpeakingBase')
    },
    // {
    //     path: '/add_speaking',
    //     name: 'AddSpeaking',
    //     component: () => import('@/components/Subcomponents/DesignExam/speaking/AddSpeaking')
    // },
    // {
    //     path: '/edit_speaking',
    //     name: 'EditSpeaking',
    //     component: () => import('@/components/Subcomponents/DesignExam/speaking/EditSpeaking')
    // },
    {
        path: '/writing',
        name: 'Writing',
        component: () => import('@/components/Subcomponents/DesignExam/writing/WritingBase')
    },
    // {
    //     path: '/add_writing',
    //     name: 'AddWriting',
    //     component: () => import('@/components/Subcomponents/DesignExam/writing/AddWriting')
    // },
    // {
    //     path: '/edit_writing',
    //     name: 'EditWriting',
    //     component: () => import('@/components/Subcomponents/DesignExam/writing/EditWriting')
    // },
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

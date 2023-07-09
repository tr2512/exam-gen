import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import About from '../views/About.vue'
import SignUp from '../views/SignUp.vue'
import LogIn from '../views/LogIn.vue'

import Courses from '../views/Courses.vue'
import Course from '../views/Course.vue'
import QuestionDatabase from '../views/QuestionDatabase.vue'
import ExamGen from '../views/ExamGen.vue'
import CreateCourse from '../views/CreateCourse.vue'
import EditCourse from '../views/EditCourse.vue'
import MyAccount from '../views/dashboard/MyAccount.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/about',
    name: 'About',
    component: About
  },
  {
    path: '/sign-up',
    name: 'SignUp',
    component: SignUp
  },
  {
    path: '/log-in',
    name: 'LogIn',
    component: LogIn
  },
  {
    path: '/courses',
    name: 'Courses',
    component: Courses
  },
  {
    path: '/courses/:slug',
    name: 'Course',
    component: Course
  },

  {
    path: '/dashboard/my-account',
    name: 'MyAccount',
    component: MyAccount
  },
    {
        path: '/courses/:slug/question-database',
        name: 'QuestionDatabase',
        component: QuestionDatabase
      },

      {
        path: '/courses/:slug/exam-gen',
        name: 'ExamGen',
        component: ExamGen
      },
    {
        path: '/courses/create-course',
        name: 'CreateCourse',
        component: CreateCourse
    },
    {
        path: '/courses/edit-course/:slug',
        name: 'EditCourse',
        component: EditCourse
    }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router

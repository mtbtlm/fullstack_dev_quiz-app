import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '../views/HomePage.vue'
import NewQuizPage from '../views/NewQuizPage.vue'
import LoginPage from '../views/LoginPage.vue'
import AdminSection from '../views/AdminSection.vue'
import QuestionManager from '../views/QuestionManager.vue'
import ScorePage from '../views/ScorePage.vue'
import Logout from '../views/Logout.vue'
import AboutView from '../views/AboutView.vue'
import QuestionEditorPage from '../views/QuestionEditor.vue'
import PostQuestionPage from '../views/PostQuestionPage.vue'
import ModifyQuestion from '../views/ModifyQuestion.vue'
import ShowQuestionsPage from '../views/ShowQuestionsPage.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'Quiz App',
      component: HomePage
    },
    {
      path: '/quiz',
      name: 'Quiz',
      component: QuestionManager
    },
    {
      path: '/admintools',
      name: 'Administration',
      component: AdminSection
    },
    {
      path: '/showquestions',
      name: 'Liste des questions',
      component: ShowQuestionsPage
    },
    {
      path: '/newquiz',
      name: 'Commencer le quiz',
      component: NewQuizPage
    },
    {
      path: '/about',
      name: 'A propos',
      component: AboutView
    },
    {
      path: '/login',
      name: 'Connexion',
      component: LoginPage
    },
    {
      path: '/logout',
      name: 'Logout',
      component: Logout,
    },
    {
      path: '/postquestion',
      name: 'Ajouter une question',
      component: PostQuestionPage
    },
    {
      path: '/modifyquestion',
      name: 'Modifier une question',
      component: ModifyQuestion
    },
    {
      path: '/editor',
      name: 'Détail de la question',
      component: QuestionEditorPage
    },
    {
      path: '/score',
      name: 'Score',
      component: ScorePage
    },
  ]
})

router.beforeEach((to, from, next) => {
  document.title = to.name;
  next();
});

export default router

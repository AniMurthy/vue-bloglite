import { createRouter, createWebHistory } from "vue-router"

import Profile from './components/ProfilePage.vue'
import Posts from './components/PostsPage.vue'
import Follows from './components/FollowersPage.vue'
import Feed from './components/FeedPage.vue'
import Login from './components/LoginPage.vue'
import Signup from './components/SignupPage.vue'
import Search from './components/SearchPage.vue'
import CreatePost from './components/CreatepostPage.vue'
import Authorprofile from './components/AuthorProfilePage.vue'
import Editpost from './components/EditpostPage.vue'

const routes = [
    {
        path:'/feed',
        name:'feed',
        component:Feed,

    },
    {
        path:'/profile',
        name:'profile',
        component:Profile,

    },
    {
        path:'/posts',
        name:'posts',
        component:Posts,

    },
    {
        path:'/follows',
        name:'follows',
        component:Follows

    },
    {
        path:'/',
        name:'login',
        component:Login

    },
    {
        path:'/signup',
        name:'signup',
        component:Signup

    },
    {
        path:'/author/posts/create',
        name:'createposts',
        component:CreatePost,

    },
    {
        path:'/search',
        name:'search',
        component:Search,

    },
    {
        path:'/author/profile/:id',
        name:'authorprofile',
        component:Authorprofile,
        props:true

    },
    {
        path:'/posts/edit/:id',
        name:'editpost',
        component:Editpost,
        props:true

    }
]

const router = createRouter({
    history:createWebHistory(),
    routes,
})

export default router;
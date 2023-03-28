<template>
    <div class="container-fluid mx-5 my-5">
        <h4>FEED</h4>
        <hr/>
        <div v-if="this.token == null">
        <h5>Please Login First</h5>
        <router-link to="/" class="btn btn-primary mr-2">Login</router-link>
        </div>
        <div v-else>
            <div v-if="posts.length" class="row row-cols-1 row-cols-md-3 g-4">
                <div v-for="post in posts" :key="post.post_id" >
                    <div class="col">
                        <div class="card h-700" style="height: 30rem;">
                            <div class="card-body overflow-auto">
                                <h5 class="card-title">{{post.Title}}</h5>
                                <p class="card-text " v-for="paragraph in post.Content" :key="paragraph.id">{{paragraph}}</p>
                            </div>
                            <div class="card-footer">
                                <p v-if="post.author_id==post.currid">Author: {{ post.Author_name }}</p>
                                <p v-else>
                                    Author: <router-link :to="{name:'authorprofile',
                                    params:{id:post.author_id}}"
                                    style="text-decoration:none;">{{ post.Author_name }}</router-link>
                                </p>
                                <p><u>Published on:</u> {{post.Date}}</p>
                                <p v-if="post.Date_m"><u>Date modified:</u> {{post.Date_m}}</p>
                            </div>
                        </div>
                    </div> 
                </div> 
            </div>
            <div v-else>
                <h5 class="text-center align-middle fs-1">Nothing to see here</h5>
            </div>
        </div>
        </div>
</template>

<script>
export default {
    data() {
        return {
            posts:[],
        }
    },
    methods:{
        getPosts(){
            fetch('http://127.0.0.1:5000/post',{
                method:"GET",
                headers:{
                    "Content-Type":"application/json",
                    "Access-Control-Allow-Origin": "*",
                    "Authentication_token":localStorage.getItem("auth_token")
                }
        })
        .then(resp => resp.json())
        .then(data =>{
            this.posts.push(...data)
      })
        .catch( error => {
            console.log(error)
            })
        },
        getVal(){
            this.token=localStorage.getItem("auth_token")
            if(this.token){
                this.getPosts()
            }
        },
    },
    created() {
        this.getVal()
       },


}
</script>

<style>

</style>
<template>
  <div class="container mx-5 my-5">
    <h4>FEED</h4>
    <hr/>
    <div v-if="posts.length">
        <div v-for="post in posts" :key="post.post_id">
        <h5><u>{{post.Title}}</u></h5>
        <h6 v-if="post.author_id==post.currid">
            Author: {{ post.Author_name }}
        </h6>
        <h6 v-else>
            Author: <router-link :to="{name:'authorprofile',params:{id:post.author_id}}" class="btn btn-info my-3">{{ post.Author_name }}</router-link>
        </h6>
        <p v-for="paragraph in post.Content" :key="paragraph.id">{{paragraph}}</p>
        <p><u>Published on:</u> {{post.Date}}</p>
        <p v-if="post.Date_m"><u>Date modified:</u> {{post.Date_m}}</p>
        <hr/>
    </div> 
    </div>
    <div v-else>
        <h5>Nothing to see here</h5>
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
        }
    },
    created() {
        this.getPosts()
        // location.reload(true)
       },


}
</script>

<style>

</style>
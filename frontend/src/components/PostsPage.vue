<template>
  <div class="container-fluid mx-5 my-5">
  <h4 >My Posts</h4>
  <hr/>
  <div v-if="this.token == null">
    <h5>Please Login First</h5>
    <router-link to="/" class="btn btn-primary mr-2">Login</router-link>
    </div>
    <div v-else >
    <div class="row">
    <button class="btn btn-success col-2 mb-2 mx-2" v-on:click="createPost()">create Post</button>
    </div>
    <div v-if="posts.length" class="row row-cols-1 row-cols-md-3 g-4" >
      <div v-for="post in posts" :key="post.post_id" >
          <div class="col ">
              <div class="card" style="height: 31rem;">
                  <div class="card-body overflow-auto">
                      <h5 class="card-title">{{post.Title}}</h5>
                      <p class="card-text" v-for="paragraph in post.Content" :key="paragraph.id">{{paragraph}}</p>
                  </div>
                  <div class="card-footer overflow-x-auto" style="height: 9rem;width:auto;">
                      <p><u>Published on:</u> {{post.Date}}</p>
                      <p v-if="post.Date_m"><u>Date modified:</u> {{post.Date_m}}</p>
                      <button class="btn btn-danger" v-on:click="delPost(post.Id)">Delete Post</button>
                      <router-link :to="{name:'editpost',params:{id:post.Id}}" class="btn btn-warning mx-2">Update Post</router-link>
                  </div>
              </div>
          </div>
      </div>
    </div> 
    <!-- <div v-if="posts.length">
      <div v-for="post in posts" :key="post.Id">
          <h5><u>{{post.Title}}</u></h5>
            <p v-for="paragraph in post.Content" :key="paragraph.id">
              {{paragraph}}
            </p>
            <p><u>Published on:</u> {{post.Date}}</p>
            <p v-if="post.Date_m"><u>Date modified:</u> {{post.Date_m}}</p>
            <button class="btn btn-danger mr-3" v-on:click="delPost(post.Id)">Delete Post</button>
            <router-link :to="{name:'editpost',params:{id:post.Id}}" class="btn btn-warning mx-3">Update Post</router-link>
            <hr/>
        </div> 
      </div> -->
    <div v-else>Pease create a post</div>
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
    props:{
    auth_id:{
      type:[Number,String],
      requried:true
    },
    post_id:{
      type:[Number,String],
      requried:true
    }
  },
    methods:{
        getAuthorPosts(){
            fetch(`http://127.0.0.1:5000/author/post`,{
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
            this.getAuthorPosts()
          }
        },
        delPost(post_id){
          if(confirm("are you sure you want to delete this post?"))
            {fetch(`http://127.0.0.1:5000/author/post/${post_id}/delete`,{
              method:"POST",
              headers:{
                "Content-Type":"application/json",
                "Access-Control-Allow-Origin": "*",
                "Authentication_token":localStorage.getItem("auth_token")
                }
              })
              .then(resp => resp.json())
              .then(()=>{
                location.reload()
              })
              .catch(error => {
                console.log(error)
              })
            }
    },
    createPost(){
      this.$router.push({
        name:'createposts'
      })
    },
    
    },
    created() {
        this.getVal()
       }

}
</script>

<style>

</style>
<template>
  <div class="container-fluid mx-5 my-5" >
    <h4>Profile page</h4>
    <hr/>
    <div v-if="this.token == null">
    <h5>Please Login First</h5>
    <router-link to="/" class="btn btn-primary mr-2">Login</router-link>
    </div>
    <div v-else>
        <div class="card text-bg-light mb-3" style="max-width: 540px;">
        <div class="row g-0">
          <div class="col-md-4">
            <svg xmlns="http://www.w3.org/2000/svg" width="100%" height="100%" fill="currentColor" class="bi bi-person-circle" viewBox="-.5 -.5 17 17">
              <path d="M11 6a3 3 0 1 1-6 0 3 3 0 0 1 6 0z"/>
              <path fill-rule="evenodd" d="M0 8a8 8 0 1 1 16 0A8 8 0 0 1 0 8zm8-7a7 7 0 0 0-5.468 11.37C3.242 11.226 4.805 10 8 10s4.757 1.225 5.468 2.37A7 7 0 0 0 8 1z"/>
            </svg>
          </div>
          <div class="col-md-8">
            <div class="card-body">
              <h5 class="card-title"><u>Userame:</u> {{author.Name}}</h5>
              <p class="card-text"><u>Email_id:</u> {{author.Author_Email}}</p>
              <div v-if="author.followMe">
                <p>You're already followng this author</p>
                <p class="col my-3"><button class="btn btn-danger" v-on:click="unfollow(author.Author_id)">unfollow</button></p>
            </div>
            <div v-else>
                <button type="submit" class="btn btn-warning" v-on:click="follow(author.Author_id)">Follow</button>
            </div>
            </div>
          </div>
        </div>
      </div>
      <div class="row row-cols-1 row-cols-md-3 g-4">
        <div class="card text-bg-light col mx-3 my-3" style="max-width: 25rem;">
          <div class="card-body">
            <h3 class="card-title text-center text-dark align-middle">Number of posts</h3>
            <br>
            <p class="card-text text-center text-dark fs-1">{{author.no_posts}}</p>
          </div>
        </div>
        <div class="card text-bg-light col mx-3 my-3" style="max-width: 25rem;">
          <div class="card-body">
            <h3 class="card-title text-center text-dark align-middle">Number of following</h3>
            <br>
            <p class="card-text text-center text-dark fs-1">{{author.no_follows}}</p>
          </div>
        </div>
        <div class="card text-bg-light col mx-3 my-3" style="max-width: 25rem;">
          <div class="card-body">
            <h3 class="card-title text-center text-dark align-middle">Number of followers</h3>
            <br>
            <p class="card-text text-center text-dark fs-1">{{author.no_following}}</p>
          </div>
        </div>
      </div>
        <div v-if="author.no_posts==0">
            <h3 class="display-3">No posts yet</h3>
        </div>
        <div v-else>
            <h3 class="display-3">Posts</h3>
            <div v-for="post in author.posts" :key="post.id" class="row row-cols-1 row-cols-md-3 g-4">
                <div class="col">
                    <div class="card h-100">
                        <div class="card-body">
                            <h5 class="card-title">{{post.Title}}</h5>
                            <p class="card-text " v-for="paragraph in post.Content" :key="paragraph.id">{{paragraph}}</p>
                        </div>
                        <div class="card-footer">
                            <p><u>Published on:</u> {{post.Date}}</p>
                            <p v-if="post.Date_m"><u>Date modified:</u> {{post.Date_m}}</p>
                        </div>
                    </div>
                </div> 
            </div>
        </div>
        
    </div>
  </div>
</template>

<script>
export default {
    data() {
        return{
            author:{}
        }
    },
    props:{
        id:{
            type:[String,Number],
            required:true
        }
    },
    methods:{
        follow(user_id){
          fetch(`http://127.0.0.1:5000/author/follow/${user_id}`,{
                method:"POST",
                headers:{
                    "Content-Type":"application/json",
                    "Access-Control-Allow-Origin": "*",
                    "Authentication_token":localStorage.getItem("auth_token")
                }
        })
        .then(resp => resp.json())
        .then(()=>{
          this.$router.push({
            name:'follows'
          })
        })
        .catch( error => {
            console.log(error)
            })
        },
        getVal(){
            this.token=localStorage.getItem("auth_token")
            if(this.token){
                this.get_dets(`${this.id}`)
            }
        },
        get_dets(id){
            fetch(`http://127.0.0.1:5000/author/profile/${id}`,{
                method:"GET",
                headers:{
                    "Content-Type":"application/json",
                    "Access-Control-Allow-Origin": "*",
                    "Authentication_token":localStorage.getItem("auth_token")
                }
        })
        .then(resp => resp.json())
        .then(data=>{
            this.author=data
        })
        .catch( error => {
            console.log(error)
            })
        },
        unfollow(id){
          fetch(`http://127.0.0.1:5000/author/unfollow/${id}`,{
                method:"POST",
                headers:{
                    "Content-Type":"application/json",
                    "Access-Control-Allow-Origin": "*",
                    "Authentication_token":localStorage.getItem("auth_token")
                }
        })
        .then(resp => resp.json())
        .then(()=>{
          this.$router.push({
            name:'follows'
          })
        })
        .catch( error => {
            console.log(error)
            })
        }
    },
    created(){
        this.getVal()
    }

}
</script>

<style>

</style>
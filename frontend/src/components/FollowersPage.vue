<template>
  <div class="container-fluid mx-5 my-5">
    <div class="row">
      <div>
        <h4>Followers and Following</h4>
        <hr/>
        <div v-if="this.token == null">
        <h5>Please Login First</h5>
        <router-link to="/" class="btn btn-primary mx-2">Login</router-link>
        </div>
        <div v-else class="row">
          <div class="col mx-5">
          <h5>Who I'm Following</h5>
          <hr/>
          <div v-if="follows.length" class="row row-cols-1 row-cols-lg-2 g-4">
            <div v-for="follow in follows" :key="follow.id">
              <div class="card text-bg-light col my-3">
                <router-link :to="{name:'authorprofile',params:{id:follow.id}}" style="text-decoration:none">
                  <div class="card-body">
                    <h3 class="card-title text-center text-dark align-middle">{{ follow.name }}</h3>
                  </div>
                  <div class="card-footer text-center ">
                    <p><button class="btn btn-danger align-middle" v-on:click="unfollow(follow.id)">unfollow</button></p>
                  </div>
                </router-link>
              </div>
            </div>
          </div>
          <div v-else>
            <p>You're not following anyone</p>
          </div>
          </div>
          <div class="col mx-5" >
            <div>
              <h5>Who is Following Me</h5>
              <hr/>
              <div v-if="following.length" class="row row-cols-1 row-cols-lg-2 g-4">
                <div v-for="follow in following" :key="follow.id">
                  <div class="card text-bg-light col my-3">
                    <router-link :to="{name:'authorprofile',params:{id:follow.id}}" style="text-decoration:none">
                      <div class="card-body">
                        <h3 class="card-title text-center text-dark align-middle">{{ follow.name }}</h3>
                      </div>
                    </router-link>
                  </div>
                  <!-- <router-link :to="{name:'authorprofile',params:{id:follow.id}}" class="btn btn-primary my-3 col">{{ follow.name }}</router-link> -->
                </div>
              </div>
              <div v-else>
                <p>No one is following you</p>
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
        return {
            follows:[],
            following:[]
        }
    },
    methods:{
        getFollows(){
            fetch('http://127.0.0.1:5000/author/following',{
                method:"GET",
                headers:{
                    "Content-Type":"application/json",
                    "Access-Control-Allow-Origin": "*",
                    "Authentication_token":localStorage.getItem("auth_token")
                }
        })
        .then(resp => resp.json())
        .then(data =>{
            this.following.push(...data)
      })
        .catch( error => {
            console.log(error)
            })
        },
        getVal(){
          this.token=localStorage.getItem("auth_token")
          if(this.token){
            this.getFollows(),
            this.getFollowing()
          }
        },
        getFollowing(){
            fetch('http://127.0.0.1:5000/author/followers',{
                method:"GET",
                headers:{
                    "Content-Type":"application/json",
                    "Access-Control-Allow-Origin": "*",
                    "Authentication_token":localStorage.getItem("auth_token")
                }
        })
        .then(resp => resp.json())
        .then(data =>{
            this.follows.push(...data)
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
          location.reload()
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
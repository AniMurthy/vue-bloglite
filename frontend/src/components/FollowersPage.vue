<template>
  <div class="container mx-5 my-5">
    <div class="row">
      <div class="col" >
        <h4>Who I'm Following</h4>
        <hr/>
        <div v-if="this.token == null">
    <h5>Please Login First</h5>
    <router-link to="/" class="btn btn-primary mr-2">Login</router-link>
    </div>
    <div v-else>
      <div v-if="follows.length">
        <div class="row"  v-for="follow in follows" :key="follow.id">
          <router-link :to="{name:'authorprofile',params:{id:follow.id}}" class="btn btn-primary my-3 col">{{ follow.name }}</router-link>
          <p class="col my-3"><button class="btn btn-warning" v-on:click="unfollow(follow.id)">unfollow</button></p>
        </div>
      </div>
      <div v-else>
        <p>You're not following anyone</p>
      </div>
      <div class="col" >
        <div class="col">
          <h4>Who is Following Me</h4>
          <hr/>
          <div v-if="following.length">
            <div class="row" v-for="follow in following" :key="follow.id">
              <router-link :to="{name:'authorprofile',params:{id:follow.id}}" class="btn btn-primary my-3 col">{{ follow.name }}</router-link>
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
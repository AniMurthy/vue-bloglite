<template>
  <div class="container my-5 mx-5" >
  <nav class="navbar navbar-expand bg-body-primary">
  <div class="container">
    <router-link class="navbar-brand" to="/feed">Blog</router-link>
    <div class="collapse navbar-collapse" id="navbarSupportedContent">
      
      <ul class="navbar-nav me-auto mb-2 mb-lg-0">
        <li class="nav-item">
            <router-link class="nav-link" to="/profile">Profile</router-link>
        </li>
        <li class="nav-item">
            <router-link class="nav-link"  to="/posts">Posts</router-link>
        </li>
        <li class="nav-item">
            <router-link class="nav-link"  to="/follows">Follows</router-link>
        </li>
        <li class="nav-item">
            <router-link class="nav-link"  to="/search">search</router-link>
        </li>
      </ul>
        <form @submit.prevent="logout">
        <button class="btn btn-danger mx-2">logout</button>
      </form>
      <div v-if="!chk">
        <router-link to='/' class="btn btn-success mx-2" >login</router-link>
      </div>
    </div>
  </div>
    
</nav>
</div>
</template>

<script>
export default {
  data(){
    return{chk:null}
  },
        methods:{
          logout(){
            fetch('http://127.0.0.1:5000/logout',{
                method:"POST",
                headers:{
                    "Content-Type":"application/json",
                    "Access-Control-Allow-Origin": "*",
                },
                })
                .then(resp => resp.json())
                .then(() =>{
                    localStorage.removeItem("auth_token")
                    // window.location.reload()
                    this.$router.push({
                    name:'login'
                  })
              })
              .catch( error => {
                    console.log(error)
                })
          },
          check(){
            if(localStorage.getItem("auth_token")===null){
              this.chk= false
            }
            else{
              this.chk= true
            }
          }
          
        },
        beforeMount(){
          this.check()
        }
}
</script>

<style>

</style>
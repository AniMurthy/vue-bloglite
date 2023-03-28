<template>
    <div class="conatiner-fluid mx-5 my-5">
      <h4>Sign up for the Blog</h4>
      <hr/>
      <form>
        <div class="row mb-3">
          <label for="Email" class="col-sm-2 col-form-label">Name</label>
          <div class="col-sm-10">
            <input type="text" class="form-control" id="name" v-model="username">
          </div>
        </div>
        <div class="row mb-3">
          <label for="Email" class="col-sm-2 col-form-label">Email</label>
          <div class="col-sm-10">
            <input type="email" class="form-control" id="Email" v-model="email">
          </div>
        </div>
        <div class="row mb-3">
          <label for="Password" class="col-sm-2 col-form-label">Password</label>
          <div class="col-sm-10">
            <input type="password" class="form-control" id="Password" v-model="password" autocomplete="on">
          </div>
        </div>
        <div class="row mb-3">
          <label for="Password" class="col-sm-2 col-form-label">Re-enter Password</label>
          <div class="col-sm-10">
            <input type="password" class="form-control" id="RePassword" v-model="repassword" autocomplete="on">
          </div>
        </div>
        <router-link to="#"  type="submit" class="btn btn-primary" v-on:click="signup()">Sign up</router-link>
      </form>
    </div>
</template>
  
  <script>
  export default {
    data(){
        return{
            email:null,
            password:null,
            repassword:null,
            username:null,
            err:null
        }
    },
    methods:{
        signup(){
          console.log(this.password)
                fetch('http://127.0.0.1:5000/register',{
                method:"POST",
                headers:{
                    "Content-Type":"application/json",
                    "Access-Control-Allow-Origin": "*",
                    },
                body:JSON.stringify({username:this.username,email:this.email,password:this.password})
                })
                .then(resp => resp.json())
                .then(()=>{
                    this.$router.push({
                        name:'login'
                    })
                })
                .catch( error => {
                    console.log(error)
                    })
        }
    }
  
  }
  </script>
  
  <style>
  
  </style>
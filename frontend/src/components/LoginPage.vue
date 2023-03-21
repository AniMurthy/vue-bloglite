<template>
    <div class="conatiner mx-5 my-5">
      <h4>Login</h4>
      <hr/>
      <form>
        <label for="Email">Email</label>
        <input type="email" class="form-control mb-3" id="Email" autocomplete="on" v-model="email">
        <label for="Password">Password</label>
        <input type="password" class="form-control mb-3" id="Password" autocomplete="on" v-model="password">
        <router-link to="/" type="submit" class="btn btn-primary mr-3" v-on:click="login()">log in</router-link>
      </form>
      <form>
        <router-link to="/signup" class="btn btn-info my-3">signup</router-link>
      </form>
      <div v-if="err" class="alert alert-warning alert dismissable fade show mt-5" role="alert">
            <strong>{{ err }}</strong>
        </div>
  </div>
</template>

<script>
export default {
    data() {
        return {
            email:null,
            password:null,
            err:null           
        }
    },
    methods:{
      login(){ 
        if(this.email||this.password){
                  fetch('http://127.0.0.1:5000/login?include_auth_token',{
                    method:"POST",
                    headers:{
                      "Content-Type":"application/json",
                      "Access-Control-Allow-Origin": "*",
                    },
                    body:JSON.stringify({"email":this.email,"password":this.password})
                    })
                    .then(resp => resp.json())
                    .then(data =>{
                      if(data.meta.code==200){
                          localStorage.setItem("auth_token", data['response']['user']['authentication_token'])
                          this.$router.push({
                          name:'feed'
                          })
                      }
                      else{
                        this.err=(data.response.errors)
                      }
                        })
                    .then(
                        )
                    .catch( error => {
                          console.log(error)
                      })}
                      else{
                        this.err="Fields should not be empty"
                      }
                },
              signup(){
                this.$router.push({
                          name:'signup'
                        })
              }
            }
 
}
</script>

<style>

</style>
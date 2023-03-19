<template>
  <div class="container my-5 mx-5" >
    <h4>Profile page</h4>
    <hr/>
      <form @submit.prevent="uploadImage" enctype="multipart/form-data">
        <input type="file" name="image">
        <button type="submit" class="btn btn-success my-2">Upload</button>
      </form>
        <h5><u>Userame:</u> {{author.Name}}</h5>
        <p><u>Email_id:</u> {{author.Author_Email}}</p>
        <router-link to="/posts" class="btn btn-primary mr-2">Number of posts: {{author.no_posts}} </router-link>
        <router-link to="/follows" class="btn btn-primary mx-2">Number of followers: {{author.no_follows}}</router-link>
        <router-link to="/follows" class="btn btn-primary mx-2">Number of following: {{author.no_following}}</router-link>
    <div>
      <form @submit.prevent="delProfile">
      <button type="submit" class="btn btn-danger my-2">Delete account</button>
    </form>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return{
      author:{},
    }
  },
  props:{
    auth_id:{
      type:[Number,String],
      requried:true
    }
  },

  methods:{
    getProfile(){
      fetch(`http://127.0.0.1:5000/author`,{
        method:"GET",
        headers:{
          "Content-Type":"application/json",
          "Access-Control-Allow-Origin": "*",
          "Authentication_token":localStorage.getItem("auth_token")
        }
      })
      .then(resp => resp.json())
      .then(data =>{
        this.author = data
      })
      .catch(error => {
            console.log(error)
            })
    },
    delProfile(){
      fetch(`http://127.0.0.1:5000/author/delete`,{
        method:"POST",
        headers:{
          "Content-Type":"application/json",
          "Access-Control-Allow-Origin": "*",
          "Authentication_token":localStorage.getItem("auth_token")
        }
      })
      .then(resp => resp.json())
      .then(()=>{
            localStorage.removeItem("auth_token")
            this.$router.push({
              name:'signup'
            })
      })
      .catch(error => {
            console.log(error)
            })
    }
  },
  created() {
      this.getProfile()
    }

}
</script>

<style>

</style>
<template>
  <div class="container-fluid mx-5 my-5">
    <div class="mb-3">
      <label for="Title" class="form-label" >Title</label>
      <input class="form-control" id="Title" v-model="title">
    </div>
    <div class="mb-3">
        <label for="Content" class="form-label">Content</label>
        <textarea class="form-control" id="Content" rows="10" v-model="content"></textarea>
        <form @submit.prevent="createPost">
            <button type="submit" class="btn btn-danger">Publish</button>
        </form>
    </div>
    <div v-if="err" class="alert alert-warning mt-5" role="alert">
      <strong>{{ err }}</strong>
    </div>
  </div>
</template>

<script>

export default {
    data() {
    return{
      title:null,
      content:null,
      err:null

    }
  },
  methods:{
    createPost(){
      if(this.title && this.content){
        fetch(`http://127.0.0.1:5000/author/post`,{
          method:"POST",
          headers:{
            "Content-Type":"application/json",
            "Access-Control-Allow-Origin": "*",
            "Authentication_token":localStorage.getItem("auth_token")
          },
          body:JSON.stringify({"title":this.title,"content":this.content})
        })
        .then(resp => resp.json())
        .then(()=>{
              this.$router.push({
                name:'posts'
              })
        })
        .catch(error => {
              console.log(error)
              })
      }
      else{
        this.err="Fields should not be empty"
      }
    }
    }
}
</script>

<style>

</style>
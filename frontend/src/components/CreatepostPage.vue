<template>
    <div class="container mt-5">
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
</div>
</template>

<script>
export default {
    data() {
    return{
      title:"",
      content:""
    }
  },
  methods:{
    createPost(){
      fetch(`http://127.0.0.1:5000/author/post`,{
        method:"POST",
        headers:{
          "Content-Type":"application/json",
          "Access-Control-Allow-Origin": "*",
          "Authentication_token":localStorage.getItem("auth_token")
        },
        body:JSON.stringify({title:this.title,content:this.content})
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
    }
}
</script>

<style>

</style>
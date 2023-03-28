<template>
  <div class="container-fluid mx-5 my-5">
    <h4>Update your post</h4>
    <hr/>
  <label for="Title" class="form-label mt-3 h5" >Title</label>
  <input class="form-control" id="Title" v-model="title">
    <label for="Content" class="form-label mt-3 h5">Content</label>
    <textarea class="form-control" id="Content" rows="10" v-model="content"></textarea>
    <button type="submit" class="btn btn-success my-3" v-on:click="updatePost(id)">Update</button>
</div>
</template>

<script>
export default {
    data() {
        return{
            post:[],
            title:'',
            content:'',
        }
    },
    props:{
        id:{
            type:[String,Number],
            required:true
        }
    },
    methods:{
        getPost(id){
            fetch(`http://127.0.0.1:5000/author/post/${id}/edit`,{
                method:"GET",
                headers:{
                    "Content-Type":"application/json",
                    "Access-Control-Allow-Origin": "*",
                    "Authentication_token":localStorage.getItem("auth_token")
                }
        })
        .then(resp => resp.json())
        .then(data =>{
            this.post.push(...data)
            this.title=data[0].title
            data[0].content.forEach(element => {
                this.content+=element+'\n'
            });

      })
        .catch( error => {
            console.log(error)
            })
        },
        updatePost(id){
            fetch(`http://127.0.0.1:5000/author/post/${id}/edit`,{
                method:"POST",
                headers:{
                    "Content-Type":"application/json",
                    "Access-Control-Allow-Origin": "*",
                    "Authentication_token":localStorage.getItem("auth_token")
                },
                body:JSON.stringify({title:this.title,content:this.content})
        })
        .then(resp => resp.json())
        .then(() =>{
            this.$router.push({
                name:'posts'
            })
      })
        .catch( error => {
            console.log(error)
            })
        },
    },
    created(){
        this.getPost(`${this.id}`)
    }

}
</script>

<style>

</style>
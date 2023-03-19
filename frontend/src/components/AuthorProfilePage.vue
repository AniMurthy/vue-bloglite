<template>
  <div class="container mx-5 my-5" >
    <h4>Profile page</h4>
    <hr/>
    <div>
        <h5><u>Author name:</u> {{ author.Name }}</h5>
        <h5><u>Email:</u> {{ author.Author_Email }}</h5>
        <h5><u>Number of Posts:</u> {{ author.no_posts }}</h5>
        <h5><u>Number following:</u> {{ author.no_following }}</h5>
        <h5><u>Number of followers:</u> {{ author.no_follows }}</h5>
        <div v-if="author.no_posts==0">
            <p>No posts yet</p>
        </div>
        <div v-else>
            <h5><u>Posts</u></h5>
            <div v-for="post in author.posts" :key="post.id">
                <h6><u>{{ post.Title }}</u></h6>
            <p v-for="paragraph in post.Content" :key="paragraph.id">{{paragraph}}</p>
            </div>
        </div>
        <div v-if="author.followMe">
            <p>You're already followng this author</p>
        </div>
        <div v-else>
            <button type="submit" class="btn btn-warning" v-on:click="follow(author.Author_id)">Follow</button>
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
        .catch( error => {
            console.log(error)
            })
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
        }
    },
    created(){
        this.get_dets(`${this.id}`)
    }

}
</script>

<style>

</style>
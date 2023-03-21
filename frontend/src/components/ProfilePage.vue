<template>
  <div class="container my-5 mx-5" >
    <h4>Profile page</h4>
    <hr/>
    <!-- <img :src="thumbnailUrl" class="img-fluid "> -->
      <form @submit.prevent="uploadImage" enctype="multipart/form-data">
        <input type="file" ref="image">
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
      propic:"tempic.png"
    }
  },
  // props:{
  //   auth_id:{
  //     type:[Number,String],
  //     requried:true
  //   }
  // },
  computed: {
    thumbnailUrl() {
      return this.propic ? URL.createObjectURL(this.propic) : 'tempic.png';
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
    },
    // uploadImage(){
    //   this.propic = this.$refs.image
    //   console.log(this.propic.files[0])

    // },
    // getImage(){
    //   fetch(`http://127.0.0.1:5000/author/pic`,{
    //     method:"GET",
    //     headers:{
    //       "responseType":"blob",
    //       "Access-Control-Allow-Origin": "*",
    //       "Authentication_token":localStorage.getItem("auth_token")
    //     },
    //   })
    //   .then(response => {
    //     response.json()
    //     this.propic=this.convertToBlob(response.pic)
    //     console.log(response)
    //   })
    //   .catch(error => {
    //         console.log(error)
    //         })

    // },
    // convertToBlob(base64Data) {
    //   const byteCharacters = atob(base64Data);
    //   const byteArrays = [];

    //   for (let i = 0; i < byteCharacters.length; i++) {
    //     byteArrays.push(byteCharacters.charCodeAt(i));
    //   }

    //   const blob = new Blob([new Uint8Array(byteArrays)], {type: 'image/jpeg'});
    //   return blob;
    // }
  },
  created() {
      this.getProfile()
      // this.getImage()
    }

}
</script>

<style>

</style>
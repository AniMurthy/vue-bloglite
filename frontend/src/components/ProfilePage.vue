<template>
  <div class="container-fluid  my-5 mx-5" >
    <h4>Profile page</h4>
    <hr/>
    <div v-if="this.token == null">
    <h5>Please Login First</h5>
    <router-link to="/" class="btn btn-primary mr-2">Login</router-link>
    </div>
    <div v-else>
      <div class="card text-bg-light mb-3" style="max-width: 540px;">
        <div class="row g-0">
          <div class="col-md-4">
            <svg xmlns="http://www.w3.org/2000/svg" width="100%" height="100%" fill="currentColor" class="bi bi-person-circle" viewBox="-.5 -.5 17 17">
              <path d="M11 6a3 3 0 1 1-6 0 3 3 0 0 1 6 0z"/>
              <path fill-rule="evenodd" d="M0 8a8 8 0 1 1 16 0A8 8 0 0 1 0 8zm8-7a7 7 0 0 0-5.468 11.37C3.242 11.226 4.805 10 8 10s4.757 1.225 5.468 2.37A7 7 0 0 0 8 1z"/>
            </svg>
          </div>
          <div class="col-md-8">
            <div class="card-body">
              <h5 class="card-title"><u>Userame:</u> {{author.Name}}</h5>
              <p class="card-text"><u>Email_id:</u> {{author.Author_Email}}</p>
            </div>
          </div>
        </div>
      </div>
      <div class="row row-cols-1 row-cols-md-3 g-4">
        <div class="card text-bg-light col mx-3 my-3" style="max-width: 25rem;">
          <router-link to="/posts" style="text-decoration:none">
          <div class="card-body">
            <h3 class="card-title text-center text-dark align-middle">Number of posts</h3>
            <br>
            <p class="card-text text-center text-dark fs-1">{{author.no_posts}}</p>
          </div>
        </router-link>
        </div>
        <div class="card text-bg-light col mx-3 my-3" style="max-width: 25rem;">
          <router-link to="/follows" style="text-decoration:none">
          <div class="card-body">
            <h3 class="card-title text-center text-dark align-middle">Number of following</h3>
            <br>
            <p class="card-text text-center text-dark fs-1">{{author.no_follows}}</p>
          </div>
        </router-link>
        </div>
        <div class="card text-bg-light col mx-3 my-3" style="max-width: 25rem;">
          <router-link to="/follows" style="text-decoration:none">
          <div class="card-body">
            <h3 class="card-title text-center text-dark align-middle">Number of followers</h3>
            <br>
            <p class="card-text text-center text-dark fs-1">{{author.no_following}}</p>
          </div>
        </router-link>
        </div>
      </div>
        <!-- <router-link to="/posts" class="card text-bg-dark col mx-3 my-3" style="max-width: 20rem;">Number of posts: {{author.no_posts}} </router-link>
        <router-link to="/follows" class="btn btn-primary mx-2">Number of following: {{author.no_follows}}</router-link>
        <router-link to="/follows" class="btn btn-primary ml-2">Number of followers: {{author.no_following}}</router-link> -->
    <div>
      <button v-on:click="getReport()" class="btn btn-info">Generate PDF report</button>
      <button class="btn btn-info mx-2" v-on:click="exportcsv()">Export Posts as csv</button>
      <form @submit.prevent="delProfile">
      <button type="submit" class="btn btn-danger my-2">Delete account</button>
      </form>
    </div>
  </div>
  </div>
</template>

<script>
export default {
  data() {
    return{
      author:{},
      propic:"tempic.png",
      token:null
    }
  },
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
        // console.log(localStorage.getItem("auth_token"))
      })
      .catch(error => {
            console.log(error)
            })
    },
    getVal(){
      this.token=localStorage.getItem("auth_token")
      if(this.token){
        this.getProfile()
      }
    },
    getReport(){
      fetch(`http://127.0.0.1:5000/report`,{
        method:"GET",
        headers:{
          "Content-Type":"application/json",
          "Access-Control-Allow-Origin": "*",
          "Authentication_token":localStorage.getItem("auth_token")
        }
      })
      .then(resp=> {
         resp.json();
         alert("PDF Report Generated");
      })
      .catch(error => {
            console.log(error)
            })

    },
    exportcsv(){
      fetch(`http://127.0.0.1:5000/DownloadCSV`,{
                method:"GET",
                headers:{
                    "Content-Type":"text/csv",
                    "Access-Control-Allow-Origin": "*",
                    "Authentication_token":localStorage.getItem("auth_token"),
                    "Content-disposition":"attachment filename=userposts.csv"
                }
        })
        .then(resp=> {
         resp.json();
         alert("CSV Generated");
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
      this.getVal()
    }

}
</script>

<style>

</style>
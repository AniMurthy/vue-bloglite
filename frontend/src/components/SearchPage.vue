<template>
    <div class="container-fluid mx-5 my-5">
            <h4>Search for an author</h4>
            <hr/>
        <div v-if="this.token == null">
            <h5>Please Login First</h5>
            <router-link to="/" class="btn btn-primary mr-2">Login</router-link>
        </div>
        <div v-else class="conatiner-fluid mx-2 my-3">
            <form >
                <input class="form-control" placeholder="Enter username to be searched" v-model="partial">
                <button class="btn btn-success my-3" v-on:click.prevent="search">Search</button>
            </form>
            <div class="conatiner my-3" v-if="results.length">
                <div class="col" v-for="result in results" :key="result.id">
                    <div class="card text-bg-light my-3" style="max-width: 25rem;">
                    <router-link :to="{name:'authorprofile',params:{id:result.id}}" style="text-decoration:none">
                      <div class="card-body">
                        <h3 class="card-title text-center text-dark align-middle">{{ result.name }}</h3>
                      </div>
                      <div class="card-footer text-center">
                        <div v-if="result.following">
                            <p>You're already followng this author</p>
                        </div>
                        <div v-else>
                            <button type="submit" class="btn btn-warning" v-on:click="follow(result.id)">Follow</button>
                        </div>
                      </div>
                    </router-link>
                  </div>
                </div>
            </div>
            <div v-if="err" class="alert alert-warning mt-5" role="alert">
                <strong>{{ err }}</strong>
            </div>
        </div>
</div>
</template>

<script>
export default {
    data() {
        return {
            partial:null,
            results:[],
            err:''
        }
    },
    methods:{
        search(){
            if (!this.partial){
                this.err='Search field cannot be left empty'
            }
            else{
                this.err=''
            fetch('http://127.0.0.1:5000/author/search',{
                    method:"POST",
                    headers:{
                      "Content-Type":"application/json",
                      "Access-Control-Allow-Origin": "*",
                      "Authentication_token":localStorage.getItem("auth_token")
                    },
                    body:JSON.stringify({"partial":this.partial}),
                    })
                    .then(resp => resp.json())
                    .then(data =>{
                        this.results=[],
                        this.results.push(...data)
                    })
                    .then(()=>{
                        this.$router.push({
                            name:'search'
                        })
                    })
                    .catch(error =>{
                        console.log(error)
                    })
                }

        },
        getVal(){
            this.token=localStorage.getItem("auth_token")
        },
        follow(id){
          fetch(`http://127.0.0.1:5000/author/follow/${id}`,{
                method:"POST",
                headers:{
                    "Content-Type":"application/json",
                    "Access-Control-Allow-Origin": "*",
                    "Authentication_token":localStorage.getItem("auth_token")
                }
        })
        .then(resp => resp.json())
        .then(()=>{
            this.$router.push({
              name:'follows'
            })
        })
        .catch( error => {
            console.log(error)
            })
        }

    },
    created() {
        this.getVal()
       }

}
</script>

<style>

</style>
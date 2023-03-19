<template>
    <div class="conatiner mx-5 my-5">
        <h4>Search for an author</h4>
        <hr/>
        <form >
        <input class="form-control me-2" placeholder="Enter username to be searched" v-model="partial">
        <button class="btn btn-success my-3" v-on:click.prevent="search">Search</button>
        </form>
        <div class="conatiner my-3" v-if="results.length">
            <div class="col" v-for="result in results" :key="result.id">
                <router-link :to="{name:'authorprofile',params:{id:result.id}}" class="btn btn-primary mr-3">{{ result.name }}</router-link>
                <button class="btn btn-warning mx-3" v-on:click="follow(result.id)">Follow</button>
            </div>
        </div>
        <div v-if="err" class="alert alert-warning alert dismissable fade show mt-5" role="alert">
            <strong>{{ err }}</strong>
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

    }

}
</script>

<style>

</style>
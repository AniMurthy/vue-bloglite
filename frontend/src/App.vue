<template>
  <div id =app>
    <NavigationBar />
    <router-view/>
  </div>
</template>

<script>
import NavigationBar from './components/NavigationBar.vue'
export default {
  name:'App',
  components:{
    NavigationBar
  },
  methods:{
    check(){
      if(localStorage.getItem('auth_token')){
        return true
      }
      else{
        return false
      }
    }
  }

}
</script>

<style>

</style>
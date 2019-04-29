<template>
  <div id="app">
    <visualization></visualization>
    <ImportData></ImportData>
    <!-- <img src="./assets/logo.png">
    <router-view/> -->
  </div>
</template>

<script>
import visualization from './components/Visualization/visualization.vue'
import ImportData from './components/Import/ImportData.vue'
export default {
  name: 'App',
  components: {
    visualization,
    ImportData
  }}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>

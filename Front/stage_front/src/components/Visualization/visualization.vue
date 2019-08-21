<template>
  <header>
    <h1>Animal Movement Cleaner Application</h1>
    <a href="#">
      HELP
    </a>
  </header>
</template>

<script>
import Vue from 'vue'
import VueCesium from 'vue-cesium'
// Vue-Cesium will load Cesium.js from `https://unpkg.com/cesium/Build/Cesium/Cesium.js`
Vue.use(VueCesium, {
  // cesiumPath is path of Cesium.js', for example:
  // local Cesium Build package:
  // cesiumPath: './static/Cesium/Cesium.js'
  // Official Online Cesium Build package：
  cesiumPath: 'https://unpkg.com/cesium/Build/Cesium/Cesium.js'
})
export default{
}
</script>

<style>
header{
  background: #111;
  padding: 0px;
  text-align: left;
  color: #6eb0ed;
  display: inline-flex;
  justify-content: space-between;
  width: 100%;
  position: fixed;
  left: 0;
  top: 0;
  right: 0;
  z-index: 9999;
}
header h1{
  font-size: 2em;
  padding: 10px 20px;
  margin: 0px;
}
header a{
  background-color: #1b568c;
  color: #fff;
  font-weight: bold;
  padding: 0px 50px;
  display: flex;
  align-items: center;
}
header a:hover{
  color: #fff;
  background-color: #2367a5;
  text-decoration: none;
}
</style>

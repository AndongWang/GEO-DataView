<template>
  <!-- <img alt="Vue logo" src="./assets/logo.png"> -->
  <MapComponentV2/>
</template>

<script>
// import MapComponent from './components/MapComponent.vue';
import MapComponentV2 from './components/DragableMapComponent.vue';

export default {
  name: 'App',
  components: {
    // MapComponent,
    MapComponentV2,
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
</style>

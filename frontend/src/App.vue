<script >
import Navbar from './components/Navbar.vue';
import Footer from './components/Footer.vue';
export default {
  
  data() {
    return {};
  },
  components: {
    Navbar,
    Footer,
  },
};
</script>

<template>
  <div id="div" class="container-full">
  <Navbar />
  <div class="rv-container">
  <router-view />
  </div>
  <Footer />
  </div>
</template>

<style scoped>
.container-full {
  min-height: 100vh;
  background-color: antiquewhite;

}
.rv-container{
  min-height: 85vh;

}


</style>
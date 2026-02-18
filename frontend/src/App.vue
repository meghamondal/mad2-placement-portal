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
  <Navbar />
  <div class="router-view-container">
  <router-view />
  </div>
  <Footer />
</template>

<style scoped>
.router-view-container{
  min-height: 89vh;

}
</style>
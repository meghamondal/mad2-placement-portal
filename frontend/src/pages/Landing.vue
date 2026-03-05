<script>

export default {
  name: "Landing",
  data () {
  },
  methods: {
    goToLogin() {
      this.$router.push('/login')
    }

  }
};

</script>

<template>
  <div>
    <div class="overlay"></div>
    <div class="photo-container"></div>
    <div class="login-box col-md-6 d-flex justify-content-center">
    <div id="login-container">
        Welcome to Placement Portal App
      <a class="btn btn-primary" href="/login" @click="goToLogin">Login</a>
      <br>
      <br>
      <p style="font-size: 1.1rem;">Discover paths, connect with companies, and shape tomorrow's success.</p>
    </div>
    </div>
  </div>

</template>

<style scoped>
.photo-container {
  width: 100%;
  height: 89vh;
  background-image: url('../../landing_image/landing_page.jpg');
  background-repeat: no-repeat;
  background-size: cover;
  background-position: 1rem -40rem;
}

.login-box {
  position: absolute;
  z-index: 20;
  left: 65rem;
  bottom: 10rem;
  border: 3px solid aqua;
  border-radius: 2rem;
  padding: 2rem;
  backdrop-filter: blur(1rem);
  color: white;
  font-size: 1.4rem;
  width: 28rem;
  }

  .overlay {
    position: absolute;
    width: 100%;
    height: 90vh;
    z-index: 10;
    background-color: black;
    opacity: 60%;
    
   
  }
</style>
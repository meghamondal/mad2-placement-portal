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
  <section>
    <div class="container">
      <div class="row min-vh-100 d-flex align-items-center">
        <div class="col-md-6">Left</div>
        <div class="col-md-6 d-flex justify-content-center">
          <div id="main">
            <div id="main2"></div>
            <div id="login-container">
              Welcome to Placement Portal App
              <a href="/login" @click="goToLogin">Login</a>
              <p>Discover paths, connect with companies, and shape tomorrow's success.</p>
            </div>
          </div>
        </div>
      </div>
    </div>
</section>
</template>
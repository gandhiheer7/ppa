<template>
  <Navbar />
  <div class="container mt-4">
    <router-view />
  </div>
</template>

<script>
import Navbar from './components/Navbar.vue';

export default {
  components: {
    Navbar
  }
};
</script>

<style>
/* Global styles if needed, but we rely on Bootstrap */
</style>
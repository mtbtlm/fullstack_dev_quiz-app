<script setup>
import { RouterLink, RouterView } from 'vue-router'
import adminStorageService from "@/services/AdminStorage";
function isConnected() {
  return adminStorageService.getToken() === '' ? false : true
}
</script>

<template>
    <header class="w-100">
    <nav class="navbar navbar-expand-lg navbar-light">
      <RouterLink class="nav-item nav-link active" to="/">Home</RouterLink>
      <RouterLink class="nav-item nav-link active" to="/about">About</RouterLink>
      <RouterLink class="nav-item nav-link active" to="/admintools">Manage</RouterLink>
      <RouterLink class="nav-item nav-link active" v-if="isConnected()" :key="$route.fullPath" to="/logout">Log out
      </RouterLink>
      <RouterLink class="nav-item nav-link active" v-if="!isConnected()" :key="$route.fullPath" to="/login">Login
      </RouterLink>
    </nav>
  </header>
  <RouterView />
  
</template>

<style>
nav {
  display: flex;
  align-items: center;
  position: fixed;
}

header {
  height: fit-content;
}

nav a {
  font-size: 2rem;
  margin: 1rem 0;
  margin-left: 1rem;
  margin-right: 1rem;
}


nav a:hover {
  transform: scale(1.225);
  transition-duration: 1s;
}
</style>


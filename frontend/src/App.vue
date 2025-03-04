<template>
  <div>
    <router-view />
    <Toaster position="top-right" />
  </div>
</template>
<script setup>
import { Toaster } from 'vue-sonner';
</script>

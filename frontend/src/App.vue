<template>
  <div id="app">
    <header class="app-header">
      <h1>{{ appTitle }}</h1>
    </header>
    <main class="app-main">
      <p>projectAlpha 开发中...</p>
    </main>
  </div>
</template>

<script setup>
const appTitle = import.meta.env.VITE_APP_TITLE || 'projectAlpha'
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  background-color: #f5f5f5;
  color: #333;
}

#app {
  min-height: 100vh;
}

.app-header {
  background-color: #4a90d9;
  color: white;
  padding: 16px 24px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.app-header h1 {
  font-size: 24px;
  font-weight: 600;
}

.app-main {
  padding: 24px;
}
</style>

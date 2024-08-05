<!-- 
Credit for this CSS loader
https://cssloaders.github.io/ 
-->
<template>
    <div class="container">
        <span class="loader"></span>
        <p class="help">Loading..</p>
    </div>
</template>
<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
    name: 'PageLoader',
});
</script>
<style scoped>
.container{
    z-index: 999;
    position: fixed;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    height: 100vh;
    width: 100vw;
    background-color: rgba(173, 217, 255, 0.37);
}
.help{
    margin-top: 15px;
}
.loader {
    width: 48px;
    height: 48px;
    display: inline-block;
    position: relative;
}
.loader::after,
.loader::before {
    content: '';  
    box-sizing: border-box;
    width: 48px;
    height: 48px;
    border: 2px solid #134b70;
    position: absolute;
    left: 0;
    top: 0;
    animation: scaleOut 2s ease-in-out infinite;
}
.loader::after {
    border-color: #FF3D00;
    animation-delay: 1s;
}

@keyframes scaleOut {
    0% {
        transform: scale(0);
    }
    100% {
        transform: scale(1);
    }
}
</style>
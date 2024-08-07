<template>
    <div class="home-container">
        <h1>Home</h1>
        <p>Welcome to your personnal local AI chat</p>
    </div>

    <div id="icon-links">
        <a href="https://github.com/Roy-Bivash/pulsar" target="_blank">
            <img class="icon" :src="githubIcon" alt="">
        </a>
    </div>
</template>
<script lang="ts">
import githubIcon from "@/assets/icons/github.png";
export default {
    name: "Home",
    data(){
        return {
            githubIcon
        };
    }
}
</script>
<style scoped>
.home-container{
    margin: 0;
    padding: 20px 25px;
    display: flex;
    flex-direction: column;
    /* background-color: aliceblue; */
    height: 100%;
    /* width: 100%; */
}

#icon-links{
    position: absolute;
    top: 15px;
    right: 15px;
}
.icon{
    aspect-ratio: 1/1;
    height: 30px;
    cursor: pointer;
    transition: 0.2s all ease-in-out;
}
.icon:hover{
    transform: scale(1.1);
}
</style>
  
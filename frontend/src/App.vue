<script setup lang="ts">
import { ref, onMounted, provide } from "vue";
import SideBar from "@/components/sideBar/SideBar.vue";
import { CustomFetch } from "@/modules/CustomFetch.ts";
import PageLoader from "@/components/loader/pageLoader/PageLoader.vue";
import { setPageLoading, usePageLoading } from "@/modules/pageLoading.ts";
import ErrorModal from "@/components/modal/errorModal/ErrorModal.vue";

interface errorModalInterface {
  show: boolean,
  content: string
}

const allChats = ref<Array<chat>>([]);
const errorModal = ref<errorModalInterface>({ show:false, content: "" });
provide('updateChatList', getAllChat);

interface chat {
  id:number,
  name: string
}

async function getAllChat() {
  setPageLoading(true);
  const { response, error } = await CustomFetch('/chat', { method: 'GET' });
  if(error) {
    console.error(error);
    setPageLoading(false);
    return errorModal.value = { show: true, content: "Internal server error : Server not responding" }
  }
  allChats.value = response;
  setPageLoading(false);
}

onMounted(getAllChat);

const { isLoading } = usePageLoading();
</script>
<template>
  <PageLoader v-if="isLoading" />
  <div class="container">
    <SideBar :historyData="allChats" />
    <main>
      <router-view />
    </main>
  </div>
  <ErrorModal
    v-if="errorModal.show"
    @close="errorModal.show = false"
  >
    {{ errorModal.content }}
  </ErrorModal>
</template>

<style scoped>
.container{
  display: flex;
  height: 100vh;
  width: 100%;
  overflow-y: hidden;
}
main{
  height: 100%;
  width: 100%;
}
</style>

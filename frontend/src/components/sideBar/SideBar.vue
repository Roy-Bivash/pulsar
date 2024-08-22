<template>
    <nav>
        <h1  id="title">
            <router-link to="/">Chat</router-link>
        </h1>
        <div class="nav-btn-container">
            <button 
                v-on:click="newChatModalRef.show = true"
                class="nav-btn" 
                type="button"
            >
                New Chat
                <img class="btn-icon" :src="editIcon" alt="icon">
            </button>
            <!-- <button class="nav-btn" type="button">Account</button> -->
        </div>
        <History :current="chatId" :historyData="historyData" />
        <Modal 
            v-if="newChatModalRef.show"
            title="New Chat" 
            @close="newChatModalRef.show = false"
        >
            <form @submit.prevent="submitForm">
                <p>Name of chat</p>
                <input 
                    v-model="newChatModalRef.name"
                    class="name-input"
                    type="text" 
                    placeholder="New Chat"
                >
                <p>Add your system prompt here</p>
                <input 
                    v-model="newChatModalRef.prompt"
                    class="prompt-input"
                    type="text" 
                    placeholder="You are a helpful AI assistant."
                >
                <br>
                <button type="submit" class="btn-prompt-submit">Confirm</button>
            </form>
        </Modal>
        <ErrorModal
            v-if="errorModal.show"
            @close="errorModal.show = false"
        >
            {{ errorModal.content }}
        </ErrorModal>
    </nav>
</template>

<script lang="ts">
import { defineComponent, PropType, onMounted, ref, watch, inject } from 'vue';
import { useRoute } from 'vue-router';
import Modal from "@/components/modal/Modal.vue";
import { CustomFetch } from "@/modules/CustomFetch.ts";
import { setPageLoading } from "@/modules/pageLoading.ts";
import ErrorModal from "@/components/modal/errorModal/ErrorModal.vue";


import History from "./history/History.vue";
import editIcon from "@/assets/icons/edit.png";

interface HistoryItem {
    id: number;
    name: string;
}

interface newChatModalInterface{
    show: boolean,
    name: string,
    prompt: string
}

interface errorModalInterface {
  show: boolean,
  content: string
}


export default defineComponent({
    name: "SideBar",
    components: {
        History,
        Modal,
        ErrorModal
    },
    props: {
        historyData: {
            type: Array as PropType<HistoryItem[]>,
            required: true
        }
    },
    setup() {
        const route = useRoute();
        const chatId = ref<number>(0);
        const newChatModalRef = ref<newChatModalInterface>({ show: false, name:"New Chat", prompt:"You are a helpful AI assistant."});
        const updateChatListProvider = inject('updateChatList') as Function;
        const errorModal = ref<errorModalInterface>({ show:false, content: "" });



        const updateChatId = () => {
            const rawId = route.params.id as string | undefined;
            if (rawId) {
                chatId.value = parseInt(rawId, 10);
            }
        };

        onMounted(updateChatId);

        watch(
            () => route.params.id,
            updateChatId
        );


        async function submitForm() {
            setPageLoading(true);
            
            if(newChatModalRef.value.prompt === "" && !newChatModalRef.value.prompt && newChatModalRef.value.prompt.trim() === ""){
                setPageLoading(false);
                return errorModal.value = { show: true, content: "Input error : incorrect form input" }
            }

            const { error } = await CustomFetch(`/chat`, { 
                method: 'POST',
                body: JSON.stringify({
                    name: newChatModalRef.value.name,
                    prompt: newChatModalRef.value.prompt
                }),
                headers: {
                    'Content-Type': 'application/json'
                }
            });

            if (error) {
                setPageLoading(false);
                return errorModal.value = { show: true, content: "Internal server error : Server not responding" }
            }

            // Close the modal
            newChatModalRef.value.show = false;

            // update the chat list
            // this.$emit('update-chat-list');
            updateChatListProvider();

            setPageLoading(false);
        }

        return {
            chatId,
            newChatModalRef,
            editIcon,
            errorModal,
            submitForm
        }
    }
});
</script>

<style scoped>
nav {
    width: 250px;
    padding: 10px  20px;
    border-right: 1px solid rgba(88, 88, 88, 0.507);
    overflow-x: auto;
    scrollbar-color: #134b704d transparent;
    scrollbar-width: thin;
    box-shadow: 3px 10px 15px -3px rgba(0,0,0,0.1);
}

#title{
    margin: 20px 0;
}

#title a{
    text-decoration: none;
    color: black;
}

.nav-btn-container{
    display: flex;
    flex-direction: column;
    width: 100%;
    gap: 6px;
}

.nav-btn{
    display: flex;
    justify-content: space-between;
    align-items: center;
    background-color: transparent;
    padding: 8px 15px;
    border: none;
    cursor: pointer;
    border-bottom: 1px solid #134b7027;
    transition: all 0.07s ease-out;
}
.nav-btn:hover{
    background-color: #134b70;
    color: white;
    border-bottom: 1px solid transparent;
}

.nav-btn:hover .btn-icon{
    filter: invert(1);
}

.btn-icon{
    width: 16px;
    aspect-ratio: square;
}

.prompt-input{
    padding: 6px 10px;
    border: 1px solid #134b7027;
    width: 80%;
    margin: 6px 0;
}

.name-input{
    padding: 6px 10px;
    border: 1px solid #134b7027;
    width: 80%;
    margin: 6px 0;
}

.btn-prompt-submit{
    background-color: transparent;
    border: none;
    margin-top: 10px;
    border: 1px solid #134b70;
    padding: 5px 10px;
    border-radius: 5px;
    cursor: pointer;
    transition: all 0.07s ease-out;
}

.btn-prompt-submit:hover {
    background-color: #134b70;
    color: white;
    border-bottom: 1px solid transparent;
}

</style>

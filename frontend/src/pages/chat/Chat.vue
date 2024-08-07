<template>
    <div id="chat-container">
        <div class="top-bar">
            <h1 id="title">{{ theChatInfos.name }}</h1>
            <img class="settings-btn" :src="SettingIcon" v-on:click="settingModal.show = true">
        </div>
        <div id="content">
            <Message v-for="item in messageHistoryRef" :key="item.id"
                :role="item.role"
                :content="item.content"
            />
            <MessageLoader v-if="isLoadingNewMessage"/>
        </div>
        <form @submit.prevent="submitPromptForm" class="chat-form">
            <textarea 
                v-model="newMessageInputRef" 
                @keydown="handleKeydown"
                class="chat-input" 
                type="text"
            ></textarea>
            <button class="chat-submit-btn" type="submit">Send</button>
        </form>
    </div>

    <Modal 
        v-if="settingModal.show"
        title="Chat Settings" 
        @close="settingModal.show = false"
    >
        <form @submit.prevent="submitSettingsForm">
            <p>Name</p>
            <input v-model="settingModal.name" class="form-input" type="text">
            <p>Token limit</p>
            <input v-model="settingModal.max_token" class="form-input" type="number" min="10" max="2048" step="1">
            <p>Temperature</p>
            <input v-model="settingModal.temperature" class="form-input" type="number" min="0.1" max="1" step="0.1">
            <br>
            <div class="form-btn-groupe">
                <button type="button" class="btn-form-delete" v-on:click="isOpenDeleteChatConfirm = true">Delete the chat</button>
                <button type="submit" class="btn-form-submit">Update</button>
            </div>
        </form>
    </Modal>
    <ConfirmModal
        v-if="isOpenDeleteChatConfirm"
        title="Do you realy want to delete this chat ?" 
        @close="isOpenDeleteChatConfirm = false"
        @confirm="deleteChat"
    >
    </ConfirmModal>
    <ErrorModal
        v-if="errorModal.show"
        @close="errorModal.show = false"
    >
        {{ errorModal.content }}
  </ErrorModal>
</template>

<script lang="ts">
import { defineComponent, onMounted, ref, watch, inject } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { CustomFetch } from "@/modules/CustomFetch.ts";
import { setPageLoading } from "@/modules/pageLoading.ts";

import Modal from "@/components/modal/Modal.vue";
import ConfirmModal from "@/components/modal/confirmModal/ConfirmModal.vue";
import ErrorModal from "@/components/modal/errorModal/ErrorModal.vue";

import Message from '@/components/message/Message.vue';
import MessageLoader from "@/components/loader/messageLoader/MessageLoader.vue";

import SettingIcon from "@/assets/icons/settings.png";

interface message {
    id:number | null,
    role:string,
    content:string,
}

interface chatInfos {
    id: string | null,
    max_token: number,
    name: string,
    temperature: number
}

interface settingModalInterface {
    show: boolean,
    name: string,
    max_token: number,
    temperature: number
}

interface errorModalInterface {
  show: boolean,
  content: string
}

export default defineComponent({
    name: "Chat",
    components: {
        Message,
        MessageLoader,
        Modal,
        ConfirmModal,
        ErrorModal
    },
    methods: {
        // this method is used to allow the user to add a new line using the SHIFT + ENTER key 
        handleKeydown(event: KeyboardEvent) {
            if (event.key === "Enter") {
                if (event.shiftKey) {
                // Allow new line with Shift + Enter
                return;
                } else {
                // Prevent default Enter behavior and trigger form submission
                event.preventDefault();
                this.submitPromptForm();
                }
            }
        },
    },
    setup() {
        const route = useRoute();
        const router = useRouter(); 
        const theChatInfos = ref<chatInfos>({ id: null, max_token: 100, name: "", temperature: 0.7 });
        const messageHistoryRef = ref<Array<message>>([]);
        const newMessageInputRef = ref("");
        const isLoadingNewMessage = ref<boolean>(false);
        const settingModal = ref<settingModalInterface>({ show: false, name: "", temperature: 0, max_token: 0});
        const isOpenDeleteChatConfirm = ref<boolean>(false);
        const updateChatListProvider = inject('updateChatList') as Function;
        const errorModal = ref<errorModalInterface>({ show:false, content: "" });

        /**
         * Get all the chat infos when the component is mounted
         */
        onMounted(() => {
            theChatInfos.value.id = route.params.id as string | null;
            if (theChatInfos.value.id) {
                getChatInfos(theChatInfos.value.id);
            }
        });

        /**
         * This watch for changes in the url params.
         * If the user changes chat, the frontend must get the new chat infos
         */
        watch(route, (newRoute) => {
            theChatInfos.value.id = newRoute.params.id as string | null;
            if (theChatInfos.value.id) {
                getChatInfos(theChatInfos.value.id);
            }
        }, { immediate: true });


        /**
         * This function gets the infos about the selected chat by id :
         * - Gets the messages of the chat
         * - Gets informations like the name of the chat, the token limit, temperature
         * 
         * @param id : Id of the chat that you want the infos
         */
        async function getChatInfos(id: string) {
            setPageLoading(true);
            const { response, error } = await CustomFetch(`/messages?chat_id=${id}`, { method: 'GET' });
            if (error) {
                setPageLoading(false);
                console.error(error);
                return errorModal.value = { show: true, content: "Internal server error : Server not responding" }
            }
            messageHistoryRef.value = response.messages;

            // theChatInfos.value.name = response.infos.name;
            // theChatInfos.value.max_token = response.infos.max_token;
            // theChatInfos.value.temperature = response.infos.temperature;
            theChatInfos.value = { ...theChatInfos.value, ...response.infos };

            // update the settings
            settingModal.value = { ...settingModal.value, ...response.infos };  

            setPageLoading(false);
        }

        
        async function submitPromptForm() {
            // If a new message is already loading then we don't continue :
            if(isLoadingNewMessage.value) return;

            if(newMessageInputRef.value === "" || !newMessageInputRef.value || newMessageInputRef.value.trim() === ""){
                setPageLoading(false);
                console.error("Input error");
                return errorModal.value = { show: true, content: "Input error : incorrect form input" }
            }

            // console.log(newMessage)
            messageHistoryRef.value.push({
                id:null,
                content: newMessageInputRef.value,
                role: "user",
            });
            
            // Clear the input field
            newMessageInputRef.value = "";
            
            // Set the message loading to true :
            isLoadingNewMessage.value = true;

            const { response, error } = await CustomFetch(`/generate`, { 
                method: 'POST',
                body: JSON.stringify({
                    chat_id: theChatInfos.value.id,
                    messages: messageHistoryRef.value,
                    max_new_tokens: theChatInfos.value.max_token,
                    temperature: theChatInfos.value.temperature,
                }),
                headers: {
                    'Content-Type': 'application/json'
                }
            });

            if (error) {
                setPageLoading(false);
                console.error(error);
                return errorModal.value = { show: true, content: "Internal server error : Server not responding" }
            }

            // Add the new message to the message history array
            messageHistoryRef.value.push({
                id: response.id,
                role: "assistant",
                content: response.content,
            });

            // Set the message loading to false :
            isLoadingNewMessage.value = false;
        }

        async function submitSettingsForm(){
            setPageLoading(true);

            // verify all input :
            if(settingModal.value.name === "" || !settingModal.value.name || settingModal.value.name.trim() === ""){
                setPageLoading(false);
                console.error("Name input error");
                return errorModal.value = { show: true, content: "Input error : incorrect form input" }
            }
            if(settingModal.value.max_token < 10 || settingModal.value.max_token > 2048) {
                setPageLoading(false);
                console.error("Token limit input error");
                return errorModal.value = { show: true, content: "Input error : incorrect form input" }
            }
            if(settingModal.value.temperature < 0.1 || settingModal.value.temperature > 1) {
                setPageLoading(false);
                console.error("Temperature input error");
                return errorModal.value = { show: true, content: "Input error : incorrect form input" }
            }

            const { error } = await CustomFetch(`/chat/${theChatInfos.value.id}`, { 
                method: 'UPDATE',
                body: JSON.stringify(settingModal.value),
                headers: {
                    'Content-Type': 'application/json'
                }
            });

            if (error) {
                setPageLoading(false);
                console.error(error);
                return errorModal.value = { show: true, content: "Internal server error : Server not responding" }
            }

            // After updating the backend, update the value on the frontend :
            theChatInfos.value = { ...theChatInfos.value, ...settingModal.value };
            
            // Update the chat list :
            updateChatListProvider();

            // close the modal
            settingModal.value.show = false;

            setPageLoading(false);
        }


        async function deleteChat(){
            const { response, error } = await CustomFetch(`/chat/${theChatInfos.value.id}`, { method: 'DELETE' });
            if (error) {
                setPageLoading(false);
                console.error(error);
                return errorModal.value = { show: true, content: "Internal server error : Server not responding" }
            }
            if(response.message === "success"){
                // Update the chat list :
                updateChatListProvider();

                // redirect the user to home page :
                router.push({ path: '/', replace: true })
            }
            
        }
        

        return {
            theChatInfos,
            messageHistoryRef,
            newMessageInputRef,
            isLoadingNewMessage,
            settingModal,
            isOpenDeleteChatConfirm,
            submitPromptForm,
            submitSettingsForm,
            deleteChat,
            errorModal,
            SettingIcon
        };
    }
});
</script>



<style scoped>

#chat-container{
    margin: 0;
    padding: 0;
    display: flex;
    flex-direction: column;
    /* background-color: aliceblue; */
    height: 100%;
    width: 100%;
    
}

.top-bar{
    margin: 0;
    padding: 0 25px;
    border-bottom: 1px solid #134b7027;
    
    display: flex;
    justify-content: space-between;
}

#title{
    padding: 20px 0;
}

#content {
    padding: 0 25px;
    flex: 1;
    overflow-x: auto;
    scrollbar-color: #134b704d transparent;
    scrollbar-width: thin;
}

.chat-form{
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 5px;
    outline: 1px ridge rgba(141, 141, 141, 0.6);

    background-color: rgba(214, 214, 214, 0.089);
    height: 50px;
}

.chat-input{
    width: 60%;
    height: 35px;
    padding: 5px 10px;
    border-radius: 8px;
    resize: none;
    box-sizing: border-box;
    border: 1px solid #00000048;
    font-size: 14px;
    box-shadow: 3px 10px 15px -3px rgba(0,0,0,0.1);
}
.chat-input::-webkit-scrollbar {
    display: none;
}

.chat-submit-btn{
    border: 1px solid #00000048;
    height: 35px;
    padding: 0 25px;
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.07s ease-out;
}

.chat-submit-btn:hover {
    background-color: #134b70;
    color: white;
    border-bottom: 1px solid transparent;
}

.form-input[type="text"]{
    padding: 6px 10px;
    border: 1px solid #134b7027;
    width: 90%;
    margin: 6px 0;
}
.form-input[type="number"]{
    padding: 6px 10px;
    border: 1px solid #134b7027;
    width: 20%;
    margin: 6px 0;
}

.btn-form-submit{
    background-color: transparent;
    border: none;
    margin-top: 10px;
    border: 1px solid #134b70;
    padding: 5px 10px;
    border-radius: 5px;
    cursor: pointer;
    transition: all 0.07s ease-out;
}

.btn-form-submit:hover {
    background-color: #134b70;
    color: white;
    border-bottom: 1px solid transparent;
}

.btn-form-delete{
    background-color: transparent;
    border: none;
    margin-top: 10px;
    border: 1px solid #b61515;
    padding: 5px 10px;
    border-radius: 5px;
    cursor: pointer;
    transition: all 0.07s ease-out;
}

.btn-form-delete:hover {
    background-color: #b61515;
    color: white;
    border-bottom: 1px solid transparent;
}

.settings-btn{
    height: 25px;
    cursor: pointer;
    transition: 0.1s all ease-in;
    margin: 15px 0;
}

.settings-btn:hover {
    transform: rotate(25deg);
}

.form-btn-groupe{
    display: flex;
    gap: 5px;
}
</style>
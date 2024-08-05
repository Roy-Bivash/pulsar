<template>
    <div class="modal-container">
        <div class="modal">
            <div class="modal-header">
                <h3 class="title">{{ title }}</h3>
            </div>

            <div id="modal-content">
                <slot></slot>
            </div>
            <div class="btn-goupe">
                <button type="button" class="btn cancel" @click="$emit('close')">Cancel</button>
                <button type="button" class="btn confirm" @click="$emit('confirm')">Confirm</button>
            </div>
        </div>
    </div>
</template>
  
<script lang="ts">
import { defineComponent, PropType } from 'vue';

export default defineComponent({
    name: 'ConfirmModal',
    data() {
        return{

        }
    }
});
</script>

<style scoped>
.modal-container {
    background-color: rgba(173, 217, 255, 0.37);
    position: fixed;
    min-height: 100vh;
    min-width: 100vw;
    top: 0;
    left: 0;

    display: flex;
    align-items: center;
    justify-content: center;
}

.modal {
    background-color: white;
    border: 1px solid rgba(196, 196, 196, 0.507);
    max-width: 65vw;
    min-width: 25vw;
    padding: 15px 20px;
    box-shadow: 3px 10px 15px -3px rgba(0,0,0,0.1);
    border-radius: 5px;
}

.modal-header{
    margin-bottom: 14px;
    display: flex;
    justify-content: space-between;
}


.btn-modal-close{
    background-color: transparent;
    border: none;
    border: 1px solid transparent;
    padding: 5px 10px;
    border-radius: 5px;
    cursor: pointer;
    transition: all 0.07s ease-out;
}

.btn-modal-close:hover {
    background-color: #134b70;
    color: white;
    border-bottom: 1px solid transparent;
}

.btn-goupe{
    display: flex;
    gap: 5px;
}

.btn{
    background-color: transparent;
    border: none;
    margin-top: 10px;
    padding: 5px 10px;
    border-radius: 5px;
    cursor: pointer;
    transition: all 0.07s ease-out;
}

.cancel{
    border: 1px solid #c4c4c4;
}

.confirm{
    border: 1px solid #134b70;
}

.cancel:hover{
    color: black;
    background-color: #c4c4c4;
}

.confirm:hover {
    color: white;
    background-color: #134b70;
}

</style>

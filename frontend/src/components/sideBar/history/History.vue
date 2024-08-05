<template>
    <p class="history-description">History</p>
    <ol>
        <li v-for="item in historyData" :key="item.id" :data-selected="item.id === current">
            <!-- {{ item.name }} -->
            <router-link :to="{ name: 'Chat', params: { id: item.id } }" class="full-link">
                {{ item.name }}
            </router-link>
        </li>
    </ol>
</template>

<script lang="ts">
import { defineComponent, PropType } from 'vue';

interface HistoryItem {
    id: number;
    name: string;
}

export default defineComponent({
    name: "History",
    props: {
        historyData: {
            type: Array as PropType<HistoryItem[]>,
            required: true
        },
        current: {
            type: Number as PropType<number>,
            required: false
        }
    }
});
</script>

<style scoped>
.history-description{
    color: #8a8a8a;
    margin: 35px 0 0 0;
    padding: 0 2px;
    border-bottom: 1px solid #8a8a8a5e;
    width: fit-content;
}
ol{
    list-style-type: none;
    padding: 0;
    margin: 6px 0 0 0;
}
li{
    /* Truncate the text */
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;

    padding: 6px 6px;
    cursor: pointer;
    border-radius: 4px;
    border: 1px solid transparent;
    transition: all 0.07s ease-out;
}

li[data-selected="false"]:hover{
    background-color: #134b701e;
    border: 1px solid #adadad5e;
}

li[data-selected="true"] {
    background-color: #134b701e;
    cursor: text;
}
.full-link {
  display: block;
  color: inherit;
  text-decoration: none;
  height: 100%;
  width: 100%; 
  box-sizing: border-box;
}
</style>
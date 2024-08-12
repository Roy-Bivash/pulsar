<template>
    <div class="message-container">
        <h4 class="message-role">
            {{ role }}
            <img class="edit-icon" :src="editPencilIcon" alt="">
        </h4>
        <p class="message-content" v-html="formattedContent"></p>
        <p v-if="iteration && iteration != '0'" class="message-iteration">{{ iteration || "" }}</p>
    </div>
</template>

  
<script lang="ts">
import { defineComponent, PropType } from 'vue';
import editPencilIcon from "@/assets/icons/edit-pencil.png";
import DOMPurify from 'dompurify';

export default defineComponent({
    name: 'Message',
    props: {
        role: { type: String as PropType<string>, required: true },
        content: { type: String as PropType<string>, required: true },
        iteration: { type: String as PropType<string>, required: false }
    },
    data() {
        return {
            editPencilIcon
        };
    },
    computed: {
        formattedContent(): string {
            const contentWithSingleNewlines = this.replaceDoubleNewlines(this.content);
            const contentWithWrappedCodeSnippets = this.wrapCodeSnippets(contentWithSingleNewlines);
            return this.sanitizeContent(contentWithWrappedCodeSnippets);
        }
    },
    methods: {
        replaceDoubleNewlines(content: string): string {
            return content.replace(/\n\n/g, '\n');
        },
        wrapCodeSnippets(content: string): string {
            const codeBlockRegex = /```(.*?)```/gs;
            return content.replace(codeBlockRegex, (_match, p1) => {
                return `<pre><code>${p1}</code></pre>`;
            });
        },
        sanitizeContent(content: string): string {
            return DOMPurify.sanitize(content);
        }
    }
});
</script>



<style scoped>
.message-container{
    padding: 15px 10px 5px 10px;
    border-bottom: 1px solid #134b7027;
}

.message-role{
    text-transform: capitalize;
    margin-bottom: 4px;
}

.message-role:hover .edit-icon{
    visibility: visible;
}

.message-content{

}



.message-iteration{
    text-align: end;
}

.edit-icon{
    cursor: pointer;
    height: 15px;
    visibility: hidden;
}
</style>

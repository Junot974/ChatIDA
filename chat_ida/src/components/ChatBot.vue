<template>
  <div class="d-flex mb-6">
    <left-menu class="pa-3" :conversations="conversations" @add-conversation="addConversation" @delete-conversation="deleteConversation" @logout="logout"></left-menu>
    <chat-zone class="pa-2 align-self-start" :messages="messages" @send-message="sendMessage"></chat-zone>
  </div>
</template>


<script>
  import LeftMenu from './SideMenu.vue'
  import ChatZone from './ChatPart.vue'

  export default {
    components: {
      LeftMenu,
      ChatZone
    },
  }
</script>

<style scoped>

  left-menu {
    width: 20px;
  }

  chat-zone {
    flex-grow: 1;
  }
</style>

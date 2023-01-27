<template>
  <div>
    <left-menu :conversations="conversations" @add-conversation="addConversation" @delete-conversation="deleteConversation" @logout="logout"></left-menu>
    <chat-zone :messages="messages" @send-message="sendMessage"></chat-zone>
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

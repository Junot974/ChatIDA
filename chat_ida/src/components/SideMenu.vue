<template>
  <v-navigation-drawer v-model="drawer" app>
    <v-content>
      <v-list>
        <v-list-item v-for="conversation in conversations" :key="conversation.id">
          {{ conversation.name }}
          <v-btn color="error" @click="deleteConversation(conversation.id)">Delete</v-btn>
        </v-list-item>
      </v-list>
      <v-btn @click="addConversation" color="blue" class="padding">Add Conversation</v-btn>
    </v-content>
    <v-footer class="bottom">
      <v-btn @click="logout" color="red">Logout</v-btn>
    </v-footer>
  </v-navigation-drawer>
</template>


<script>
  export default {
  data() {
      return {
      drawer: true,
      conversations: []
      }
  },
  methods: {
      addConversation() {
      // Code pour ajouter une conversation
      },
      deleteConversation() {
      // Code pour supprimer une conversation
      // mettre id en param
      },
      logout() {
        this.$emit("logout")
      }
  },
  mounted() {
      // Code pour récupérer les conversations à partir de l'API
  }
  }
</script>

<style scoped>
  .left-menu{
  display: flex;
  flex-direction: column;
  height: 100%;
  }

  .left-menu .v-footer{
      display: flex;
      flex-direction: column;
      margin-top: auto;
  }

  .bottom{
      height: 180vh;
  }

  .padding{
      margin-left: 30px;
  }
</style>

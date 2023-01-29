<template>
  <v-navigation-drawer v-model="drawer" app>
    <v-content class="top-nav">
      <v-list>
        <v-list-item v-for="conversation in conversations" :key="conversation.id">
          <v-container class="conv-conatainer">
            {{ conversation.name }}
            <v-btn color="error" @click="deleteConversation(conversation.id)">Delete</v-btn>
          </v-container>
        </v-list-item>
      </v-list>
      <v-btn @click="addConversation" color="blue" class="padding">Add Conversation</v-btn>
    </v-content>
    <v-content class="bottom-nav">
      <v-btn @click="logout = false" color="red" @submit.prevent="logout">Logout</v-btn>
    </v-content>
  </v-navigation-drawer>
</template>


<script>
  export default {
  data() {
      return {
      drawer: true,
      conversations: [],
      logout: false,
      }
  },
  methods: {
      addConversation() {
      // Code pour ajouter une conversation
      },
      deleteConversation() {
        // /api/delete_conversation/
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
    height: 100%;
    overflow-y: scroll;
  }

  /* Style pour la zone de saisie de conversation */
  .left-menu .v-footer{
    display: flex;
    flex-direction: column;
    margin-top: auto;
  }

  /* Style pour le bouton d'ajout de conversation */
  .left-menu .v-footer .v-btn{
    margin-left: 30px;
  }
</style>

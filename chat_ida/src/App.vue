<template>
  <v-app>
    <LoginRegistrationForm v-if="!boolChat" @showChat="showChat" />
    <ChatBot v-if="boolChat" @logout="logout" @showChat="showChat"/>
  </v-app>
</template>

<script>
import LoginRegistrationForm from './components/LoginRegistrationForm.vue';
import ChatBot from './components/ChatBot.vue';
  export default {
    components: {
      LoginRegistrationForm,
      ChatBot
    },
    data: function() {
      return {
        boolChat: false,
      }
    },
    methods: {

      async showChat(){
        // console.log(this.isAuthenticated)
        // if(this.isAuthenticated){
          this.boolChat = true;
        // }
      },
      logout(){
        this.boolChat = false
      }
    }
  }
</script>


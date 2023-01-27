<template>
  <v-app>
    <div>
      <LoginRegistrationForm v-if="!boolChat" @showChat="showChat" />
      <ChatBot v-if="boolChat" @logout="logout"/>
    </div>
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
        isAuthenticated: false
      }
    },
    methods: {
      // isAuthenticate(){
      //   this.isAuthenticated = true;
      // },
      async showChat(){
        // console.log(this.isAuthenticated)
        // if(this.isAuthenticated){
          this.boolChat = true;
        // }
      },
      logout(){
        this.isAuthenticated = false,
        this.boolChat = false
      }
    }
  }
</script>


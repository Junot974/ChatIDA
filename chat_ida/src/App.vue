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
        logout: false,
      }
    },
    methods: {

      async showChat(){
          this.boolChat = true;

      },
    //   async logout(){
    //     try {
    //         const response = await fetch('/api/logout', {
    //           method: 'POST'
    //         })
    //         const data = await response.json()
    //         if (!response.ok) {
    //           throw new Error(data.message)
    //         }
    //         console.log("test")
    //         this.boolChat = false;
    //     } catch (error) {
    //         console.log(error)
    //     }
    // }
    }
  }
</script>


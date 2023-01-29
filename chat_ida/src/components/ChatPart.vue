<template>
  <v-container>
    <v-row class="padding">
      <v-col cols="12" class="chat-zone">
        <v-card class="bottom v-list">
          <v-card-title>{{ nom_conversation }} </v-card-title>
          <v-card-text >
            <v-row v-for="message in messages" :key="message.id_conv">
              <v-col cols="12" v-if="message.message_type === true">
                <div class="user-message">
                  {{ message.message }}
                </div>
              </v-col>
              <v-col cols="12" v-else>
                <div class="bot-message">
                  {{ message.message }}
                </div>
              </v-col>
            </v-row>
          </v-card-text>
          <v-card-actions class="input-zone">
            <v-text-field v-model="newMessageUser" @keyup.enter="sendMessage" :disabled="!botReplied" placeholder="Enter your message" ></v-text-field>
              <v-btn @click="sendMessage">Send</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
  export default {
      data() {
          return {
          messages: [],
          newMessageUser: '',
          nom_conversation: '',
          botReplied: true
          }
      },
      methods: {
        async sendMessage() {
          console.log(this.nom_conversation)
          try {
              const response = await fetch('/api/create_message_user', {
                  method: 'POST',
                  headers: { 'Content-Type': 'application/json' },
                  body: JSON.stringify({
                      newMessageUser: this.newMessageUser,
                  }),
              });
              if (!response.ok) {
                  throw new Error(response.statusText);
              }
              const data = await response.json();
              console.log(data)
              this.newMessageUser = ''
              this.getMessages();
              this.getConvIdAndSend();
              this.botReplied = false
          } catch (error) {
              console.error(error);
          }
        },
          async getMessages() {
            try {
              const response = await fetch('/api/get_messages', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
              })
              if (!response.ok) {
                console.log(response)
                throw new Error(response.statusText)
              }
              const data = await response.json()
              console.log(data)
              this.messages = data.map(message => {
                return {
                    id_message: message.id_message,
                    id_conv: message.id_conv,
                    message: message.message,
                    message_type: message.message_type
                }
              })
            } catch (error) {
              console.error(error)
            }
          },
          async getConvIdAndSend() {
            try {
              const response = await fetch(`/api/response_bot`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
              });
              const data = await response.json();
              this.botReplied = true
            } catch (err) {
              console.error(err);
            }
          },
          // async createConversation() {
          //   try {
          //     if (this.newMessageUser == undefined) {
          //       this.nom_conversation = "Conversation"
          //     } else {
          //       this.nom_conversation = this.newMessageUser.substring(0, this.newMessageUser.length)
          //     }
          //     const response = await fetch('/api/create_conversation', {
          //         method: 'POST',
          //         headers: { 'Content-Type': 'application/json' },
          //         body: JSON.stringify({
          //           nom_conversation: this.newMessageUser.substring(0, this.newMessageUser.length)
          //         })
          //       })
          //       if (!response.ok) {
          //           throw new Error(response.statusText);
          //       }
          //       const data = await response.json();
          //       console.log(data);
          //       this.nom_conversation = data.nom_conv
          //   } catch (error) {
          //       console.error(error);
          //   }
          // },
      },
      mounted() {
        this.getMessages()
        //this.createConversation()
        setInterval(() => {
          this.getMessages()
        }, 5000)
      },
  }
</script>

<style scoped>
  .chat-zone {
    height: 80vh;
    overflow-y: scroll;
    position: relative;
    padding-left: 9%;
    width: 100%;
  }
  .input-zone {
    position: fixed;
    bottom: 0;
    width: 80%;
  }
  .v-list {
      background-color: #f6f6f6;
  }

  .user-message {
      background-color: #4267b2;
      color: white;
      padding: 10px;
      border-radius: 10px 10px 10px 0;
      margin-bottom: 10px;
      float: right;
      clear: both;
  }

  .bot-message {
      background-color: #e6e6e6;
      color: black;
      padding: 10px;
      border-radius: 10px 10px 0 10px;
      margin-bottom: 10px;
      clear: both;
      float:left;
  }

  .v-text-field {
      width: 80%;
  }

  .padding{
    padding-left: 30px;
    width: 112%;
  }



</style>

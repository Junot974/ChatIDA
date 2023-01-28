<template>
  <v-container>
    <v-row class="padding">
      <v-col cols="12" class="chat-zone">
        <v-card class="bottom v-list">
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
            <v-text-field v-model="newMessageUser" @keyup.enter="sendMessage" placeholder="Enter your message"></v-text-field>
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
          }
      },
      methods: {
        async sendMessage() {
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
              // data.push({
              //     user: 'user',
              //     text: this.newMessageUser
              // });
              //this.messages = data
              this.newMessageUser = ''
              this.getMessages();
              this.getConvIdAndSend();
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
            let currentConvId = 1;
            if (this.messages && this.messages.length){
              for (let i = 0; i < this.messages.length; i++) {
                if (currentConvId === undefined) {
                  currentConvId = this.messages[i].id_conv;
                } else if (currentConvId !== this.messages[i].id_conv) {
                  break;
                }
              }
            }
            try {
              const response = await fetch(`/api/response_bot/${currentConvId}`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
              });
              const data = await response.json();
            } catch (err) {
              console.error(err);
            }
          }
      },
      mounted() {
        this.getMessages()
        setInterval(() => {
          this.getMessages()
        }, 5000)
      },
  }
</script>

<style scoped>
  /*.chat-zone {
  display: flex;
  flex-direction: column;
  height: 100%;
  }

  .chat-zone .v-list {
  flex: 1;
  overflow-y: auto;
  }

  .chat-zone .v-footer {
  padding: 0.5em;
  }

  .bottom{
    position: absolute;
    bottom: 0px;
    width: 50%;
    margin-left: 20%;
  } */

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

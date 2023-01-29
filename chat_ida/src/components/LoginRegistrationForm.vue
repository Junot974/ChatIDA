/* TODO : Continuer à voir les requêtes */
<template>
    <div class="center">
      <v-card class="mx-auto my-5" width="800px" transition="slide-x-transition">
        <v-card-title class="headline">{{ showRegistration ? "S'inscrire" : "Se connecter" }}</v-card-title>
        <v-card-text>
          <v-form id="registration-form" v-if="showRegistration" @submit.prevent="register" method="POST">
            <v-text-field name="username" label="Nom d'utilisateur" v-model="username" :rules="usernameRules" />
            <v-text-field name="email" label="Adresse e-mail" v-model="email" :rules="emailRules" />
            <v-text-field name="password" label="Mot de passe" v-model="password" :rules="passwordRules" type="password" />
            <v-btn type="submit" class="primary">S'inscrire</v-btn>
          </v-form>
          <v-form id="login-form" v-if="!showRegistration" @submit.prevent="login" method="POST">
            <v-text-field name="usernameOrEmail" label="Nom d'utilisateur ou adresse e-mail" v-model="usernameOrEmail" :rules="usernameOrEmailRules" />
            <v-text-field name="password" label="Mot de passe" v-model="password" :rules="passwordRules" type="password" />
            <v-checkbox v-model="rememberMe" label="Se souvenir de moi" />
            <v-btn type="submit" class="primary">Se connecter</v-btn>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-btn v-if="!showRegistration" @click="showRegistration = true" class="secondary">S'inscrire</v-btn>
          <v-btn v-if="showRegistration" @click="showRegistration = false" class="secondary">Se connecter</v-btn>
        </v-card-actions>
      </v-card>
      <v-dialog
        v-model="dialog"
        width="500"
      >
      <v-card>
          <v-card-title class="text-h5 grey lighten-2">
            Identifiants incorectes
          </v-card-title>
          <v-card-text>
            Vos identifiants de connexion ne sont pas correctes.
            Veuillez recommencer.
          </v-card-text>
          <v-divider></v-divider>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn
              color="primary"
              text
              @click="dialog = false"
            >
              OK
            </v-btn>
          </v-card-actions>
        </v-card>
        </v-dialog>
        <v-dialog
        v-model="success_registration"
        width="500"
      >
      <v-card>
          <v-card-title class="text-h5 grey lighten-2">
            Bienvenu !
          </v-card-title>
          <v-card-text>
            Vous venez de vous inscrire. Veuillez retourner sur la page de connexion.
          </v-card-text>
          <v-divider></v-divider>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn
              color="primary"
              text
              @click="success_registration = false"
            >
              OK
            </v-btn>
          </v-card-actions>
        </v-card>
        </v-dialog>
    </div>
  </template>

  <script>
    export default {
    data() {
      return {
        dialog: false,
        success_registration:false,
        // authentication: false,
        showRegistration: false,
        username: '',
        email: '',
        password: '',
        usernameOrEmail: '',
        rememberMe: false,
        usernameRules: [v => !!v || 'Le nom d\'utilisateur est requis'],
        emailRules: [v => !!v || 'L\'adresse e-mail est requise', v => /.+@.+/.test(v) || 'L\'adresse e-mail doit être valide'],
        passwordRules: [v => !!v || 'Le mot de passe est requis'],
      usernameOrEmailRules: [v => !!v || 'Le nom d\'utilisateur ou l\'adresse e-mail est requis'],
    }
  },
  methods: {
    async register() {
      try {
        const response = await fetch('/api/register', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            username: this.username,
            email: this.email,
            password: this.password
          }),
        })
        if (!response.ok) {
          console.log(response)
          throw new Error(response.statusText)
        }
        const data = await response.json()
        console.log(data)
        this.username = '';
        this.email = '';
        this.password = '';
        this.success_registration = true;

      } catch (error) {
        console.error(error)
      }
    },
    async login() {
      try {
        const response = await fetch('/api/login', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            usernameOrEmail: this.usernameOrEmail,
            password: this.password,
            rememberMe: this.rememberMe
          })
        })
        const data = await response.json()
        if (!response.ok) {
          throw new Error(data.message)
        }
          console.log("ok c'est bon")
          // this.$emit("isAuthenticated")
          this.$emit("showChat");
      } catch (error) {
        this.dialog = true;
      }
    },
  }
}
</script>

<style scoped>
.center {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100vh;
}
.headline {
  text-align: center;
}
.primary {
  background-color: blue;
  color: white;
}
.secondary {
  color: grey;
}
.slide-x-transition {
  transition: all .3s ease;
}
.slide-x-enter-active, .slide-x-leave-active {
  transition: all .3s ease;
}
.slide-x-enter, .slide-x-leave-to {
  transform: translateX(100%);
}
</style>


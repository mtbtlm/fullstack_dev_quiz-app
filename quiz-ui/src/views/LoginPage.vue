<template>

  <body>
    <div class="adminLog">
      <div class="d-flex flex-column gap-3">
      <h1>Administrator login</h1>
      <p>Enter admin password :</p>
      <input type="password" placeholder="Password" v-model="password">

      <button @click="loginwithpassword">Log in</button>

      <div v-if="errormessage != undefined && errormessage != null && errormessage != ''">
        {{ errormessage }}
      </div>
    </div>


    </div>


    
  </body>
</template>

<script>
import quizApiService from "@/services/QuizApiService";
import adminStorageService from "@/services/AdminStorage";
export default {
  name: "Login",
  data() {
    return {
      password: '',
      errormessage: ''
    }
  },
  methods: {
    async loginwithpassword() {
      var token = "";
      try {
        var response = await quizApiService.login(this.password);
        this.errormessage = '';
        token = response.data.token;
        console.log(token)
      }
      catch (e) {
        this.errormessage = "Invalid password";
        this.password = '';
      }
      finally {
        adminStorageService.saveToken(token);
        if (adminStorageService.getToken() != "")
          this.$router.push('/adminTools');
      }
    }
  }
}


</script>

<style>
.container {
  max-width: 400px;
  margin: 0 auto;
  text-align: center;
}

h1 {
  font-size: 1.5em;
  margin-bottom: 0.5em;
}

input {
  display: block;
  margin: 0 auto;
  padding: 0.5em;
  font-size: 1em;
  border: 1px solid #ddd;
}

button {
  

  padding: 15px 32px;
  text-align: center;
  display: inline-block;
  font-size: 16px;
  margin: 4px 2px;
  cursor: pointer;
}

button:hover{
  background-color: #111111;
  box-shadow: #030303 0 -6px 12px inset;
  color: #ffffff;
  border-radius: 5%;
  transform: scale(1.125);
  transition-duration: 0.5s;
}

.adminLog {
  max-width: 1000px;
  margin: 0 auto;
  text-align: center;
}
</style>



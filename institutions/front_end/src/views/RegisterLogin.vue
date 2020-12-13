<template>
  <div>
    <div id="box">
      <template>
        <v-form id="login" v-model="loginValid">
          <v-row v-if="msgLogin !== ''">
            <v-col>
              <div style="color: red; font-family: kalam;">{{ msgLogin }}</div>
            </v-col>
          </v-row>
          <v-container fluid>
            <v-row>
              <v-text-field
                  v-model="login.email"
                  label="Email"
                  style="font-family: kalam;"
                  type="email"
                  :rules="emailRules"
                  filled
                  solo-inverted
              ></v-text-field>
            </v-row>
            <v-row>
              <v-text-field
                  v-model="login.password"
                  label="Password"
                  style="font-family: kalam;"
                  type="password"
                  filled
                  solo-inverted
              ></v-text-field>
            </v-row>
            <v-row>
              <v-col>
                <v-btn color="#2F116D" style="color: white; font-family: kalam" :disabled="!loginValid"
                       @click="loginRequest">Login
                </v-btn>
              </v-col>
              <v-col>
                <v-btn text style="font-family: kalam; font-size: 12px; color: #2F116D">Forget
                  Password?
                </v-btn>
              </v-col>
            </v-row>
          </v-container>
        </v-form>
      </template>
    </div>
    <div id="overlay_box">
      <div id="teapo">TEAPO</div>
      <div id="detail">Toefl Exam And Practice Online</div>
    </div>
    <div id="top_triangle">
    </div>
    <div id="bottom_triangle">

    </div>
  </div>
</template>

<script>
import {AUTH_REQUEST} from "@/store/actions/auth";

export default {
  name: "RegisterLogin",
  data: function () {
    return {
      msgLogin: '',
      msg: '',
      login: {
        activated: false,
        email: '',
        password: '',
      },
      checkbox: false,
      valid: false,
      loginValid: false,
      emailRules: [
        v => !!v || 'E-mail is required',
        v => /.+@.+\..+/.test(v) || 'E-mail must be valid',
      ],
      options: {
        isLoggingIn: true,
        shouldStayLoggedIn: true,
      },
    }
  },
  computed: {},
  methods: {
    loginRequest() {
      const {login} = this;
      let self = this;
      console.log('salam')
      this.$store.dispatch(AUTH_REQUEST, {
        'email': login.email,
        'password': login.password,
      }).then((resp) => {
        console.log(resp)
        if (resp.data !== false) {
          this.$router.push('/');
        } else {
          self.msgLogin = 'Email or Password is Incorrect!'
        }
      })
    },

  }
}
</script>
<style scoped>

#register {
  margin-top: 40px;
  margin-left: 310px;
  margin-right: 20px;
}

#login {
  margin-top: 89px;
  margin-left: 360px;
  margin-right: 70px;
}

#login_btn {
  font-family: kalam;
  position: absolute;
  font-size: 15px;
  padding: 0;
  width: 90px;
  top: calc((100% - 393px) / 2 + 200px);
  left: calc((100% - 800px) / 2);
  text-align: center;
}

#register_btn {
  font-family: kalam;
  position: absolute;
  font-size: 15px;
  padding: 0;
  width: 90px;
  top: calc((100% - 393px) / 2 + 170px);
  left: calc((100% - 800px) / 2);
  text-align: center;
}

#detail {
  font-family: kalam;
  color: white;
  font-size: 12px;
  top: 0;
  bottom: 0;
  left: 0;
  right: 0;
  padding-top: 197.5px;
  text-align: center;
}

#teapo {
  font-family: kalam;
  position: absolute;
  color: white;
  font-weight: bold;
  top: 0;
  bottom: 0;
  left: 0;
  right: 0;
  padding-top: 170.5px;
  font-size: 26px;
  margin: auto;
  text-align: center;
}

#top_triangle {
  position: absolute;
  left: calc((100% - 800px) / 2 + 90px);
  top: calc((100% - 393px) / 2 - 150px);
  margin: auto;
  width: 0;
  height: 0;
  border-bottom: 150px solid rgb(24, 6, 80);
  border-right: 200px solid transparent;
}

#bottom_triangle {
  position: absolute;
  left: calc((100% - 800px) / 2 + 90px);
  top: calc((100% - 393px) / 2 + 393px);
  margin: auto;
  width: 0;
  height: 0;
  border-top: 150px solid rgb(24, 6, 80);
  border-left: 200px solid transparent;
}

#overlay_box {
  position: absolute;
  top: 0;
  bottom: 0;
  left: calc((100% - 800px) / 2 + 90px);
  margin: auto;
  background-color: rgb(24, 6, 80);
  width: 200px;
  height: 393px;

}

#box {
  position: absolute;
  top: 0;
  bottom: 0;
  left: 0;
  right: 0;
  margin: auto;
  background-color: rgb(229, 229, 229);
  width: 800px;
  height: 393px;
}

.disable-events {
  pointer-events: none
}

</style>

import Vue from "vue";
import Vuex from "vuex";
import dashboard from "@/store/modules/dashboard";
import reading from "@/store/modules/reading";
import auth from "@/store/modules/auth";
import user from "@/store/modules/user";

Vue.use(Vuex);

const debug = process.env.NODE_ENV !== "production";

export default new Vuex.Store({
    modules: {
        dashboard: dashboard,
        reading: reading,
        auth: auth,
        user: user,
    },
    strict: debug
});

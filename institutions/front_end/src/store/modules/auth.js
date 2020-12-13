import {
    AUTH_REQUEST,
    AUTH_ERROR,
    AUTH_SUCCESS,
    AUTH_LOGOUT,
    AUTH_FALSE
} from "../actions/auth";
import {USER_REQUEST} from "../actions/user";
import axios from 'axios'

const state = {
    token: localStorage.getItem("user-token") || "",
    status: "",
    falseCredential: false,
    hasLoadedOnce: false
};

const getters = {
    isAuthenticated: state => !!state.token,
    authToken: state => state.token
};

const actions = {
    [AUTH_REQUEST]: ({commit, dispatch}, user) => {
        return new Promise((resolve, reject) => { // The Promise used for router redirect in login
            commit(AUTH_REQUEST);
            axios({url: 'api/v1/login/', data: user, method: 'POST'})
                .then(resp => {
                    if (resp.data === false) {
                        commit(AUTH_FALSE);
                        resolve(resp)
                    } else {
                        const token = resp.data;
                        axios.defaults.headers.common['Authorization'] = `Token ${token}`;
                        localStorage.setItem('user-token', token);// store the token in localstorage
                        commit(AUTH_SUCCESS, token);
                        // you have your token, now log in your user :)
                        dispatch(USER_REQUEST);
                        resolve(resp)
                    }
                })
                .catch(err => {
                    console.log(err)
                    commit(AUTH_ERROR, err);
                    localStorage.removeItem('user-token'); // if the request fails, remove any possible user token if possible
                    reject(err)
                })
        })
    },
    [AUTH_LOGOUT]: ({commit}) => {
        return new Promise((resolve) => {
            commit(AUTH_LOGOUT);
            localStorage.removeItem('user-token'); // clear your user's token from localstorage
            localStorage.removeItem('user-id');
            console.log(localStorage.getItem("user-token"))
            resolve()
        })
    }
};

const mutations = {
    [AUTH_REQUEST]: (state) => {
        state.falseCredential = false;
        state.status = 'loading'
    },
    [AUTH_SUCCESS]: (state, token) => {
        state.status = 'success';
        state.token = token
    },
    [AUTH_ERROR]: (state) => {
        state.status = 'error'
    },
    [AUTH_LOGOUT]: state => {
        state.token = "";
    },
    [AUTH_FALSE]: state => {
        state.status = 'success';
        state.falseCredential = true;
    }
};

export default {
    state,
    getters,
    actions,
    mutations
};
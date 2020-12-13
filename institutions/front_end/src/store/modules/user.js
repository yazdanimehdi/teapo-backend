import {USER_REQUEST, USER_ERROR, USER_SUCCESS} from "../actions/user";
import {AUTH_LOGOUT} from "../actions/auth";
import axios from 'axios'

const state = {userId: 0, name: null, email: null, phone: null};

const getters = {
    getName: state => state.name,
    getId: state => state.userId,
};

const actions = {
    [USER_REQUEST]: ({commit, dispatch}) => {
        commit(USER_REQUEST);
         return new Promise((resolve, reject) => {
            axios.get('api/v1/profile/').then((resp) => {
                console.log(resp.data)
                commit(USER_SUCCESS, resp.data);
                localStorage.setItem('user-id', resp.data['id']);
                resolve(resp)
            }).catch((err) => {
                 commit(USER_ERROR);
                // if resp is unauthorized, logout, to
                dispatch(AUTH_LOGOUT);
                reject(err)
            })
        })
    },
};

const mutations = {
    [USER_REQUEST]: state => {
        state.status = "loading";
    },
    [USER_SUCCESS]: (state, resp) => {
        state.status = "success";
        state.userId = resp['id']
        state.name = resp['name']
        state.phone = resp['phone']
        state.email = resp['email']
    },
    [USER_ERROR]: state => {
        state.status = "error";
    },
    [AUTH_LOGOUT]: state => {
        state.userId = null;
        state.name = null;
        state.phone = null;
        state.email = null;
    }
};

export default {
    state,
    getters,
    actions,
    mutations
};
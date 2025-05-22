import axios from 'axios'

const URL = 'https://demo-fast-api-lms.vercel.app'
const DEBUG = true
const config = {Headers: {'Content-Type': 'application/json'}, withCredentials: true}

/**
 * 表示中のフロー情報を更新
 * @param {Flow} flow - 登録するフロー情報
 * @returns 未定
 */
export const put_flow = async (params) => {
    if(DEBUG) console.log("post_flow", params)
    await axios.put(`${URL}/flow`, params, config).then(function(response){
        if(DEBUG) console.log(response.data)
    })
    return
}

/**
 * 表示中のグループ情報を更新
 * @param {Group} group - 登録するグループ情報
 * @returns 未定
 */
export const put_group = async (params) => {
    if(DEBUG) console.log("post_group", params)
    await axios.put(`${URL}/group`, params, config).then(function(response){
        if(DEBUG) console.log(response.data)
    })
    return
}





// 型定義

/**
 * @typedef {Object} Flow - フロー情報の更新
 * @property {number} flow_id - フローのID
 * @property {string} id_in_yml - YAML内の識別ID
 * @property {string} title - フローのタイトル
 * @property {string} welcome_page_content - 演習問題開始前の説明文
 * @property {string} completion_page_content - 演習問題終了後の説明文
 * @property {number} welcome_page_content_id - 演習問題開始前の説明文のID
 * @property {number} completion_page_content_id - 演習問題終了後の説明文のID
 */

/**
 * @typedef {Object} Group - グループ情報の新規作成
 * @property {number} group_id - グループID
 * @property {string} group_name - グループ名
 * @property {number} order - グループの順番
 */
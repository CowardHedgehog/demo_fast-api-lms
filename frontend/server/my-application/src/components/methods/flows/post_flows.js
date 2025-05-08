import axios from 'axios'

const URL = 'http://localhost:8000'
const DEBUG = true
const config = {Headers: {'Content-Type': 'application/json'}, withCredentials: true}


/**
 * 表示回のフロー情報を新規登録
 * @param {Flow} flow - 登録するフロー情報
 * @returns 未定
 */
export const post_flow = async (params) => {
    if(DEBUG) console.log("post_flow", params)
    await axios.post(`${URL}/flow`, params, config).then(function(response){
        if(DEBUG) console.log(response.data)
    })
    return
}

/**
 * 表示中のグループ情報を新規登録
 * @param {Group} group - 登録するグループ情報
 * @returns 未定
 */
export const post_group = async (params) => {
    if(DEBUG) console.log("post_group", params)
    await axios.post(`${URL}/group`, params, config).then(function(response){
        if(DEBUG) console.log(response.data)
    })
    return
}

/**
 * 表示中のページ情報を新規登録
 * @param {Flowpage} flowpage - 登録するページ情報
 * @returns 未定
 */
export const post_flowpage = async (params) => {
    if(DEBUG) console.log("post_flowpage", params)
    await axios.post(`${URL}/flowpage`, params, config).then(function(response){
        if(DEBUG) console.log(response.data)
    })
    return
}


// 型定義

/**
 * @typedef {Object} Flow - フロー情報の新規作成
 * @property {number} week_id - 回のID
 * @property {string} id_in_yml - YAML内の識別ID
 * @property {string} title - フローのタイトル
 * @property {string} welcome_page_content - 演習問題開始前の説明文
 * @property {string} completion_page_content - 演習問題終了後の説明文
 */

/**
 * @typedef {Object} Group - グループ情報の新規作成
 * @property {number} flow_id - フローのID
 * @property {string} group_name - グループ名
 * @property {number} order - グループの順番
 */

/**
 * @typedef {Object} Flowpage - フローページ情報の新規作成
 * @property {number} week_id - 回のID
 * @property {number} group_id - グループのID
 * @property {string} title - ページタイトル
 * @property {number} order - ページの順番
 * @property {string} page_type - ページの種類 (SingleTextQuestion, MultipleTextQuestion, ChoiceQuestion, DescriptiveTextQuestionから)
 * @property {string} content - ページ内容
 * @property {string} hint_comment - ヒントコンテンツ
 * @property {string} answer_comment - 解答コンテンツ
 * @property {Blank_result} correct_answers - 穴埋め問題の解答
 * @property {Choice} choices - 選択問題の選択肢 *optional ChoiceQuestionのみ
 * @property {List} correct_choices - 正解の選択肢 *optional ChoiceQuestionのみ
 */

/**
 * @typedef {Object} Blank_result - 穴埋め問題の解答
 * @property {string} blank_name - 解答欄名
 * @property {string} type - 穴埋めの種類（int, float, strから）
 * @property {string} value - 解答
 * @property {string} symbol - 記号 *optional MultipleTextQuestionのみ
 */

/**
 * @typedef {Object} Choice - 選択問題の選択肢
 * @property {number} choice_id - 選択肢のID
 * @property {number} order - 選択肢の順番
 * @property {string} choice_text - 選択肢の内容
 */
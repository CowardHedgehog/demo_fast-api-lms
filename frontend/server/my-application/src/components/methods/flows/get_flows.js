import axios from 'axios'

const URL = 'https://demo-fast-api-lms.vercel.app'
const DEBUG = true



/**
 * 表示回のフロー情報を取得
 * @param {number} week_id - 回のID
 * @returns {Flow[]} - フロー情報
 */
export const get_week_flowpage = async (week_id) => {
    const flows = []
    await axios.get(`${URL}/get_week_flowpage/${week_id}`, {withCredentials: true}).then(function(response){
        flows.value = response.data
        if(DEBUG) console.log("get_week_flowpage", flows.value)
    })
    return flows.value
}











// 型定義

/**
 * @typedef {Object} Flow_id_list - フロー内でのIDリスト
 * @property {number} welcome_page_content_id - 演習問題開始前の説明文のID
 * @property {number} completion_page_content_id - 演習問題終了後の説明文のID
 */

/**
 * @typedef {Object} Flowpage_id_list - ページ内でのIDリスト
 * @property {number} origin_content_id - 元のコンテンツのID
 * @property {number} content_id - コンテンツのID
 * @property {number} origin_hint_comment_id - 元のヒントコンテンツのID
 * @property {number} hint_comment_id - ヒントコンテンツのID
 * @property {number} origin_answer_comment_id - 元の解答コンテンツのID
 * @property {number} answer_comment_id - 解答コンテンツのID
 */

/**
 * @typedef {Object} Blank_result - 穴埋め問題の解答
 * @property {number} id - 解答欄ID
 * @property {string} blank_name - 解答欄名
 * @property {string} type - 穴埋めの種類（int, float, strから）
 * @property {string} value - 解答
 * @property {string} symbol - 記号 *optional MultipleTextQuestionのみ
 */

/**
 * @typedef {Object} Choice - 選択問題の選択肢
 * @property {number} id - 選択問題ID
 * @property {number} order - 選択肢の順番
 * @property {string} content - 選択肢の内容
 */

/**
 * @typedef {Object} Flowpage - フローページ情報
 * @property {number} flowpage_id - フローページID
 * @property {string} title - ページタイトル
 * @property {string} page_type - ページの種類
 * @property {Flowpage_id_list} id_list - ページ内でのIDリスト
 * @property {string} content - コンテンツ
 * @property {string} hint_comment - ヒントコンテンツ
 * @property {string} answer_comment - 解答コンテンツ
 * @property {Blank_result[]} blank_result - 穴埋め問題の解答
 * @property {Choice[]} choices - 選択問題の選択肢 *optional ChoiceQuestionのみ
 */

/**
 * @typedef {Object} Flowpage_group - フローページグループ
 * @property {number} group_id - グループID
 * @property {string} group_name - グループ名
 * @property {number} order - 順番
 * @property {Flowpage[]} flowpages - フローページ
 */

/**
 * @typedef {Object} Flow - フロー情報
 * @property {number} flow_id - フローID
 * @property {string} id_in_yml - YAML内の識別ID
 * @property {string} flow_title - フロータイトル
 * @property {Flow_id_list} id_list - フロー内でのIDリスト
 * @property {string} welcome_page_content - 演習問題開始前の説明文
 * @property {string} completion_page_content - 演習問題終了後の説明文
 * @property {Flowpage_group[]} page_group - ページグループ
 */
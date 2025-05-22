<script setup>
// import
import axios from 'axios'
import { ref } from 'vue'
import draggable from "vuedraggable"
import MathJaxComp from '@/components/methods/MathJax.vue'
import { markdownToHtml, reloadMathJax } from '@/components/methods/markdown.js'
import { get_week_flowpage } from '@/components/methods/flows/get_flows.js'
import { post_flow, post_group, post_flowpage } from '@/components/methods/flows/post_flows.js'
import { put_flow, put_group } from '@/components/methods/flows/put_flows.js'

// variable
const props = defineProps({
  course_id: Number,
  week_id: Number
})
const flow_info = ref([])

const flow_model = ref('')
const group_model = ref('')
const page_model = ref('')
const add_content = ref(false)

const page_title = ref('')
const replace_content = ref('')
const replace_hint = ref('')
const replace_answer = ref('')
const replace_choices = ref({})

const page_type = ref(["SingleTextQuestion", "MultipleTextQuestion", "ChoiceQuestion"])
const answer_type = ref(["str", "int", "float"])

const selectedChoiceIds = ref([])

// function
const read_week_flowpage = async () => { flow_info.value = await get_week_flowpage(props.week_id) }

const add_flow = () => {
    flow_info.value.push({
        "flow_id": 0,
        "id_in_yml": "",
        "flow_title": "",
        "welcome_page_content": "",
        "completion_page_content": "",
        "page_groups": [],
    })
    flow_model.value = flow_info.value[flow_info.value.length-1]
    add_content.value = true
}

const create_flow = async () => {
    if(!validate_flow()){ return }
    const params = {
        "week_id": props.week_id,
        "id_in_yml": flow_model.value.id_in_yml,
        "title": flow_model.value.flow_title,
        "welcome_page_content": flow_model.value.welcome_page_content,
        "completion_page_content": flow_model.value.completion_page_content,
    }
    await post_flow(params)
    await read_week_flowpage()
}

const update_flow = async () => {
    if(!validate_flow()){ return }
    const params = {
        "flow_id": flow_model.value.flow_id,
        "id_in_yml": flow_model.value.id_in_yml,
        "title": flow_model.value.flow_title,
        "welcome_page_content": flow_model.value.welcome_page_content,
        "completion_page_content": flow_model.value.completion_page_content,
        "welcome_page_content_id": flow_model.value.id_list.welcome_page_content_id,
        "completion_page_content_id": flow_model.value.id_list.completion_page_content_id,
    }
    await put_flow(params)
    await read_week_flowpage()
}

const validate_flow = () => {
    if(flow_model.value.id_in_yml == ""){ alert("コンテンツ内での名称を入力してください"); return false }
    if(flow_model.value.flow_title == ""){ alert("演習問題名を入力してください"); return false }
    if(flow_model.value.welcome_page_content == ""){ alert("演習問題開始前を入力してください"); return false }
    if(flow_model.value.completion_page_content == ""){ alert("演習問題終了後を入力してください"); return false }
    return true
}



const add_group = () => {
    flow_model.value.page_groups.push({
        "group_id": 0,
        "group_name": "",
        "order": 0,
        "flowpages": [],
    })
    group_model.value = flow_model.value.page_groups[flow_model.value.page_groups.length-1]
    add_content.value = true
}

const create_group = async () => {
    if(!validate_group()){ return }
    const params = {
        "flow_id": flow_model.value.flow_id,
        "group_name": group_model.value.group_name,
        "order": group_model.value.order,
    }
    await post_group(params)
    await read_week_flowpage()
}

const update_group = async () => {
    if(!validate_group()){ return }
    const params = {
        "group_id": group_model.value.group_id,
        "group_name": group_model.value.group_name,
        "order": group_model.value.order,
    }
    await put_group(params)
    await read_week_flowpage()
}

const validate_group = () => {
    if(group_model.value.group_name == ""){ alert("グループ名を入力してください"); return false }
    if(group_model.value.order == ""){ alert("表示順を入力してください"); return false }
    if(group_model.value.order < 1 || isNaN(group_model.value.order)){ alert("表示順は1以上の整数を入力してください"); return false }
    return true
}




const add_page = () => {
    group_model.value.flowpages.push({
        "flowpage_id": 0,
        "title": "",
        "order": 0,
        "page_type": "",
        "content": "",
        "hint_comment": "",
        "answer_comment": "",
        "correct_answers": [],
        "choices": [],
        "correct_choices": [],
    })
    page_model.value = group_model.value.flowpages[group_model.value.flowpages.length-1]
    reflection_content(page_model.value.content, page_model.value.hint_comment, page_model.value.answer_comment, page_model.value.choices)
}

const create_page = async () => {
    if(!validate_page()){ return }
    const params = {
        "week_id": props.week_id,
        "group_id": group_model.value.group_id,
        "title": page_model.value.title,
        "order": parseInt(page_model.value.order),
        "page_type": page_model.value.page_type,
        "content": page_model.value.content,
        "hint_comment": page_model.value.hint_comment,
        "answer_comment": page_model.value.answer_comment,
        "correct_answers": page_model.value.correct_answers,
        "choices": page_model.value.choices,
        "correct_choices": selectedChoiceIds.value.slice().sort((a, b) => a.order - b.order).map(choice => choice.choice_id)
    }
    await post_flowpage(params)
    await read_week_flowpage()
}



const update_content = () => {
    const params = {
        "flowpage_id": page_model.value['flowpage_id'],
        "title": page_model.value['title'],
        "page_type": page_model.value['page_type'],
        "id_list": page_model.value['id_list'],
        "content": page_model.value['content'],
        "hint_comment": page_model.value['hint_comment'],
        "answer_comment": page_model.value['answer_comment'],
    }
    console.log(params)
    const config = {Headers: {'Content-Type': 'application/json'}, withCredentials: true}
    axios.post('https://demo-fast-api-lms.vercel.app/update_flowpage_content', params, config).then(function(response){
        console.log(response.data)
        read_week_flowpage()
    })
}

const validate_page = () => {
    if(page_model.value.title == ""){ alert("演習問題名を入力してください"); return false }
    if(page_model.value.page_type == ""){ alert("ページタイプを選択してください"); return false }
    if(page_model.value.content == ""){ alert("問題文を入力してください"); return false }
    if(page_model.value.hint_comment == ""){ alert("ヒントを入力してください"); return false }
    if(page_model.value.answer_comment == ""){ alert("解説を入力してください"); return false }
    return true
}


const add_answer = () => 
{
    if(["SingleTextQuestion", "single_text_question"].includes(page_model.value.page_type)) page_model.value.correct_answers.push({ "blank_name": "", "type": "", "value": "",})
    if(["MultipleTextQuestion", "multiple_text_question"].includes(page_model.value.page_type)) page_model.value.correct_answers.push({ "blank_id": "", "symble": "", "type": "", "answers": "",})
    if(["ChoiceQuestion", "choice_question"].includes(page_model.value.page_type)) page_model.value.choices.push({ "choice_id": "", "order": "", "choice_text": ""})
}

const delete_answer = (index) => { page_model.value.correct_answers.splice(index, 1) }



const clearFlowSelect = () => {
    console.log(flow_model.value)
    add_content.value = false
	group_model.value = ''
	page_model.value = ''
	replace_content.value = ''
	replace_hint.value = ''
	replace_answer.value = ''
    //if(!Reflect.has(flow_model.value, 'id_list')){ add_content.value = true }
  	if(Number(flow_model.value["flow_id"]) == 0){ add_content.value = true }
    reloadMathJax()
}

const clearGroupSelect = () => {
    add_content.value =false
	page_model.value = ''
	replace_content.value = ''
	replace_hint.value = ''
	replace_answer.value = ''
    if(Number(group_model.value["group_id"]) == 0){ add_content.value = true }
	reloadMathJax()
}







const content_replace = (content) => {
	return content
}

const reflection_content = (content, hint, answer, choices) => {
	replace_content.value = content_replace(content)
	replace_content.value = markdownToHtml(replace_content.value)
	replace_hint.value = content_replace(hint)
	replace_hint.value = markdownToHtml(replace_hint.value)
	replace_answer.value = content_replace(answer)
	replace_answer.value = markdownToHtml(replace_answer.value)
    if(page_model.value["page_type"] == "ChoiceQuestion"){
        choices.forEach((choice, index) => {
            replace_choices.value[index] = content_replace(choice.content)
            replace_choices.value[index] = markdownToHtml(replace_choices.value[index])
        })
    }
    if(page_model.value["page_type"] == "MultipleTextQuestion"){
        page_model.value.multiple_answer = page_model.value.multiple_answer.split(",")
        page_model.value.multiple_answer = page_model.value.multiple_answer.split(":")
    }
    if(Number(page_model.value["flowpage_id"]) == 0){ add_content.value = true }
    else{ add_content.value = false }
    console.log(page_model.value)
  	reloadMathJax()
}













// created
read_week_flowpage()
</script>

<template>
	<div>
        <v-row class='justify-center'>
            <!-- Flow選択 -->
            <v-col cols='4'>
                <v-autocomplete 
                    label='Flow' 
                    :items='flow_info' 
                    item-title='flow_title' 
                    item-value='flow_title' 
                    v-model='flow_model' 
                    return-object 
                    @update:modelValue='clearFlowSelect'
                >
                    <template v-slot:append-item>
                        <v-list-item @click='add_flow()'>
                            <v-list-item-title class='text-primary'><v-icon color='primary'>mdi-plus</v-icon>追加</v-list-item-title>
                        </v-list-item>
                    </template>
                </v-autocomplete>
            </v-col>
            <!-- Group選択 -->
            <v-col cols='2'>
                <v-autocomplete 
                    label='PageGroup' 
                    :items='flow_model?.page_groups' 
                    item-title='group_name' 
                    item-value='group_name' 
                    v-model='group_model' 
                    return-object 
                    @update:modelValue='clearGroupSelect' 
                    :disabled='flow_model=="" || flow_model["flow_id"]==0'
                >
                    <template v-slot:append-item>
                        <v-list-item @click='add_group()'>
                            <v-list-item-title class='text-primary'><v-icon color='primary'>mdi-plus</v-icon>追加</v-list-item-title>
                        </v-list-item>
                    </template>
                </v-autocomplete>
            </v-col>
            <!-- FlowPage選択 -->
            <v-col cols='2'>
                <v-autocomplete 
                    label='Page' 
                    :items='group_model?.flowpages' 
                    item-title='title' 
                    item-value='title' 
                    v-model='page_model' 
                    return-object 
                    :disabled='flow_model=="" || group_model=="" || group_model["group_id"]==0' 
                    @update:modelValue='reflection_content(page_model.content, page_model.hint_comment, page_model.answer_comment, page_model.choices)'
                >
                    <template v-slot:append-item>
                        <v-list-item @click='add_page()'>
                            <v-list-item-title class='text-primary'><v-icon color='primary'>mdi-plus</v-icon>追加</v-list-item-title>
                        </v-list-item>
                    </template>
                </v-autocomplete>
            </v-col>
            <!-- 操作ボタン -->
            <v-col cols='2'>
                <div v-if='page_model!=""'>
                    <div v-if='add_content'>
                        <v-btn class='justify-center my-5' @click='reflection_content(page_model.content, page_model.hint_comment, page_model.answer_comment, page_model.choices)'>反映</v-btn>
                        <v-btn class='justify-center my-5' @click='create_page()'>追加</v-btn>
                    </div>
                    <div v-else>
                        <v-btn class='justify-center my-5' @click='reflection_content(page_model.content, page_model.hint_comment, page_model.answer_comment, page_model.choices)'>反映</v-btn>
                        <v-btn class='justify-center my-5' @click='update_content()'>更新</v-btn>
                    </div>
                </div>
                <div v-else-if='group_model!=""'>
                    <div v-if='add_content'><v-btn class='justify-center my-5' @click='create_group()'>追加</v-btn></div>
                    <div v-else><v-btn class='justify-center my-5' @click='update_group()'>更新</v-btn></div>
                </div>
                <div v-else-if='flow_model!=""'>
                    <div v-if='add_content'><v-btn class='justify-center my-5' @click='create_flow()'>追加</v-btn></div>
                    <div v-else><v-btn class='justify-center my-5' @click='update_flow()'>更新</v-btn></div>
                </div>

            </v-col>
        </v-row>

        <!-- FlowPage設定 -->
        <div v-if='page_model!=""'>
            <v-row>
                <v-col cols='1'><v-card class='bg-grey-lighten-3 d-flex justify-center align-center' height='100%' variant='tonal' tile>
                        <v-card-title>問題名</v-card-title>
                </v-card></v-col>
                <v-col cols='11'><v-row><v-col cols=11><v-card class='d-flex justify-center align-center' variant='text'>
                    <v-text-field v-model='page_model.title' label='演習問題名' :disabled='page_model==""'/>
                </v-card></v-col></v-row></v-col>
            </v-row>

            <v-row>
                <v-col cols='1'><v-card class='bg-grey-lighten-3 d-flex justify-center align-center' height='100%' variant='tonal' tile>
                        <v-card-title>表示順</v-card-title>
                </v-card></v-col>
                <v-col cols='11'><v-row><v-col cols=11><v-card class='d-flex justify-center align-center' variant='text'>
                    <v-text-field v-model='page_model.order' label='表示順' :disabled='page_model==""'/>
                </v-card></v-col></v-row></v-col>
            </v-row>

            <v-row>
                <v-col cols='1'><v-card class='bg-grey-lighten-3 d-flex justify-center align-center' height='100%' variant='tonal' tile>
                        <v-card-title>形式</v-card-title>
                </v-card></v-col>
                <v-col cols='11'><v-row><v-col cols=11><v-card class='d-flex justify-center align-center' variant='text'>
                    <v-select :items='page_type' v-model='page_model.page_type' label='ページタイプ' :disabled='!add_content'/>
                </v-card></v-col></v-row></v-col>
            </v-row>
            
            <v-row>
                <v-col cols='1'><v-card class='bg-grey-lighten-3 d-flex justify-center align-center' height='100%' variant='tonal' tile>
                        <v-card-title>問題文</v-card-title>
                </v-card></v-col>
                <v-col cols='11'><v-row>
                    <v-col cols='6'><v-card class='d-flex justify-center align-center' variant='text'>
                        <v-textarea v-model='page_model.content' label='問題文' :disabled='page_model==""' auto-grow />
                    </v-card></v-col>
                    <v-col cols='6'>
                        <v-container class='mt-3'>
                            <MathJaxComp>
                                <div v-html='replace_content' />
                            </MathJaxComp>
                        </v-container>
                    </v-col>
                </v-row></v-col>
            </v-row>

            <v-row>
                <v-col cols='1'><v-card class='bg-grey-lighten-3 d-flex justify-center align-center' height='100%' variant='tonal' tile>
                        <v-card-title>ヒント</v-card-title>
                </v-card></v-col>
                <v-col cols='11'><v-row>
                    <v-col cols='6'><v-card class='d-flex justify-center align-center' variant='text'>
                        <v-textarea v-model='page_model.hint_comment' label='ヒント' :disabled='page_model==""' auto-grow />
                    </v-card></v-col>
                    <v-col cols='6'>
                        <v-container class='mt-3'>
                            <MathJaxComp>
                                <div v-html='replace_hint' />
                            </MathJaxComp>
                        </v-container>
                    </v-col>
                </v-row></v-col>
            </v-row>

            <v-row>
                <v-col cols='1'><v-card class='bg-grey-lighten-3 d-flex justify-center align-center' height='100%' variant='tonal' tile>
                        <v-card-title>解説</v-card-title>
                </v-card></v-col>
                <v-col cols='11'><v-row>
                    <v-col cols='6'><v-card class='d-flex justify-center align-center' variant='text'>
                        <v-textarea v-model='page_model.answer_comment' label='解説' :disabled='page_model==""' auto-grow />
                    </v-card></v-col>
                    <v-col cols='6'>
                        <v-container class='mt-3'>
                            <MathJaxComp>
                                <div v-html='replace_answer' />
                            </MathJaxComp>
                        </v-container>
                    </v-col>
                </v-row></v-col>
            </v-row>

            <v-row v-if='page_model.page_type == "ChoiceQuestion"'>
                <v-col cols='1'><v-card class='bg-grey-lighten-3 d-flex justify-center align-center' height='100%' variant='tonal' tile>
                        <v-card-title>選択肢</v-card-title>
                </v-card></v-col>
                <v-col cols='11'>
                    <v-row class='my-1 d-flex align-center justify-center'>
                        <v-col cols='1'>並び順　正答</v-col>
                        <v-col cols='2'>ID</v-col>
                        <v-col cols='5'>選択肢</v-col>
                        <v-col cols='4'>プレビュー</v-col>
                    </v-row>
                    <draggable v-model='page_model.choices' item-key='id' handle='.handle'>
                        <template #item='{ element }'>
                            <v-row class='drag-item bg-grey-lighten-3 my-1 d-flex align-center justify-center fill-height'>
                                <v-col cols='1'><v-row class='d-flex align-center justify-center fill-height'>
                                    <v-icon class='handle'>mdi-menu</v-icon> {{ element.order }} <v-checkbox :key='element.choice_id' :value='element' v-model='selectedChoiceIds' hide-details></v-checkbox>
                                </v-row></v-col>
                                <v-col cols='2'><v-text-field v-model='element.choice_id' hide-details></v-text-field></v-col>
                                <v-col cols='5'><v-text-field v-model='element.content' label='選択肢' hide-details/></v-col>
                                <v-col cols='4' class='bg-light-gray'><MathJaxComp><div v-html='replace_choices[element.order]'/></MathJaxComp></v-col>
                            </v-row>
                        </template>
                    </draggable>
                    <v-btn class='justify-center my-5' @click='add_answer()' :disabled='!add_content'>追加</v-btn>
                </v-col>
            </v-row>
            <v-row v-if='["SingleTextQuestion","single_text_question", "MultipleTextQuestion", "multiple_text_question"].includes(page_model.page_type)'>
                <v-col cols='1'><v-card class='bg-grey-lighten-3 d-flex justify-center align-center' height='100%' variant='tonal' tile>
                    <v-card-title>解答</v-card-title>
                </v-card></v-col>
                <v-col cols='11'>
                    <v-row class='my-1 d-flex align-center justify-center'>
                        <v-col cols='2'>ID</v-col>
                        <v-col cols='1' v-if='["MultipleTextQuestion", "multiple_text_question"].includes(page_model.page_type)'>解答欄記号</v-col>
                        <v-col cols='1'>形式</v-col>
                        <v-col>解答</v-col>
                        <v-col cols='1'>削除</v-col>
                    </v-row>
                    <v-row class='my-1 d-flex align-center justify-center' v-for='(ans, index) in page_model.correct_answers' :key="index">
                        
                        <!--v-col cols='2'><v-text-field v-model='ans.blank_name' hide-details :disabled='page_model.page_type=="SingleTextQuestion"'></v-text-field></!--v-col-->
                        <v-col cols='2'><v-text-field v-model='ans.blank_id' hide-details :disabled='!add_content || ["SingleTextQuestion", "single-text-question"].includes(page_model.page_type)'/></v-col>
                        <v-col cols='1' v-if='["MultipleTextQuestion", "multiple_text_question"].includes(page_model.page_type)'><v-text-field v-model='ans.symble' hide-details :disabled='!add_content'/></v-col>
                        <v-col cols='1'><v-select :items='answer_type' v-model='ans.type' hide-details :disabled='!add_content' /></v-col>
                        <v-col><v-text-field v-model='ans.value' label='解答' hide-details :disabled='!add_content'/></v-col>
                        <v-col cols='1'><v-btn variant='plain' @click='delete_answer(index)' :disabled='!add_content'><v-icon>mdi-close</v-icon></v-btn></v-col>
                    </v-row>
                    <v-btn class='justify-center my-5' @click='add_answer()' :disabled='!add_content'>追加</v-btn>
                </v-col>
            </v-row>
        </div>

        <!-- Group設定 -->
        <div v-else-if='group_model!=""'>
            <v-row>
                <v-col cols='2'><v-card class='bg-grey-lighten-3 d-flex justify-center align-center' height='100%' variant='tonal' tile>
                        <v-card-title>グループ名</v-card-title>
                </v-card></v-col>
                <v-col cols='10'><v-row><v-col cols=11><v-card class='d-flex justify-center align-center' variant='text'>
                    <v-text-field v-model='group_model.group_name' label='グループ名'/>
                </v-card></v-col></v-row></v-col>
            </v-row>

            <v-row>
                <v-col cols='2'><v-card class='bg-grey-lighten-3 d-flex justify-center align-center' height='100%' variant='tonal' tile>
                        <v-card-title>表示順</v-card-title>
                </v-card></v-col>
                <v-col cols='10'><v-row><v-col cols=11><v-card class='d-flex justify-center align-center' variant='text'>
                    <v-text-field v-model.number='group_model.order' label='表示順'/>
                </v-card></v-col></v-row></v-col>
            </v-row>
        </div>

        <!-- Flow設定 -->
        <div v-else-if='flow_model!=""'>
            <v-row>
                <v-col cols='2'><v-card class='bg-grey-lighten-3 d-flex justify-center align-center' height='100%' variant='tonal' tile>
                        <v-card-title>名称</v-card-title>
                </v-card></v-col>
                <v-col cols='10'><v-row><v-col cols=11><v-card class='d-flex justify-center align-center' variant='text'>
                    <v-text-field v-model='flow_model.id_in_yml' label='コンテンツ内での名称'/>
                </v-card></v-col></v-row></v-col>
            </v-row>

            <v-row>
                <v-col cols='2'><v-card class='bg-grey-lighten-3 d-flex justify-center align-center' height='100%' variant='tonal' tile>
                        <v-card-title>演習問題名</v-card-title>
                </v-card></v-col>
                <v-col cols='10'><v-row><v-col cols=11><v-card class='d-flex justify-center align-center' variant='text'>
                    <v-text-field v-model='flow_model.flow_title' label='演習問題名'/>
                </v-card></v-col></v-row></v-col>
            </v-row>

            <v-row>
                <v-col cols='2'><v-card class='bg-grey-lighten-3 d-flex justify-center align-center' height='100%' variant='tonal' tile>
                        <v-card-title>演習開始前</v-card-title>
                </v-card></v-col>
                <v-col cols='10'><v-row><v-col cols=11><v-card class='d-flex justify-center align-center' variant='text'>
                    <v-textarea v-model='flow_model.welcome_page_content' label='演習問題開始前'  auto-grow/>
                </v-card></v-col></v-row></v-col>
            </v-row>

            <v-row>
                <v-col cols='2'><v-card class='bg-grey-lighten-3 d-flex justify-center align-center' height='100%' variant='tonal' tile>
                        <v-card-title>演習終了後</v-card-title>
                </v-card></v-col>
                <v-col cols='10'><v-row><v-col cols=11><v-card class='d-flex justify-center align-center' variant='text'>
                    <v-textarea v-model='flow_model.completion_page_content' label='演習問題終了後'  auto-grow/>
                </v-card></v-col></v-row></v-col>
            </v-row>
        </div>
	</div>
</template>
<script setup>
// import
import axios from 'axios'
import { ref, watch } from 'vue'
import MathJaxComp from '@/components/methods/MathJax.vue'
import { markdownToHtml, reloadMathJax } from '@/components/methods/markdown.js'

// variable
const props = defineProps({
  course_id: Number,
  week_id: Number
})
const origin_content = ref([])
const image_dict = ref([])
const flow_dict = ref([])
const page_dict = ref([])
const content = ref('')
const pr_content = ref('')
const tab = ref(1)

// function
const get_week_origin_content = (page) => {
  axios.get(`http://localhost:8000/get_week_origin_content/${props.course_id}/${props.week_id}`, {withCredentials: true}).then(function(response){
    origin_content.value = response.data.block
    image_dict.value = response.data.image
    flow_dict.value = response.data.flow
    page_dict.value = response.data.page
    content.value = origin_content.value[page-1]['content']
    pr_content.value = content_replace(content.value)
    pr_content.value = markdownToHtml(pr_content.value)
    console.log(response.data)
    // content.value = origin_content.value[0]['content']
  })
}

const update_week_content = (content_id, origin_content_id, page) => {
  const params = {'course_id': props.course_id, 'week_id': props.week_id, 'content_id': content_id, 'origin_content_id': origin_content_id, 'content': content.value}
  console.log(JSON.stringify(params))
  const config = {headers: {'Content-Type': 'application/json'}, withCredentials: true}
  axios.post('http://localhost:8000/update_week_content', params, config).then(function(response){
    console.log(response.data)
    get_week_origin_content(page)
  })
}

const content_replace = (content) => {
  flow_dict.value.forEach(flow => {
  	const regex1 = new RegExp(`\\[(.*?)\\]\\s*\\(\\s*flow/${flow['id_in_yml']}\\s*\\)`, 'g')
  	content = content.replace(regex1, `<div class='box'><p>[$1](Flow/${flow['id']})</p></div>`)
  })
  image_dict.value.forEach(image => {
    const regex2 = new RegExp(`\\(\\s*image/${image['name']}\\s*\\)`, 'g')
    content = content.replace(regex2, `![contentsimage](http://localhost:8000/get_image/${image['id']})`)

    const regex3 = new RegExp(`\\[\\s*image/${image['name']}(.*?)\\s*\\]`, 'g')
    content = content.replace(regex3, (_, optionsStr) => {
      const widthMatch = optionsStr.match(/width=([0-9]+)/)
      const heightMatch = optionsStr.match(/height=([0-9]+)/)

      const widthAttr = widthMatch ? ` width='${widthMatch[1]}'` : ''
      const heightAttr = heightMatch ? ` height='${heightMatch[1]}'` : ''

      return `<img src='http://localhost:8000/get_image/${image.id}'${widthAttr}${heightAttr} />`
    })
  })
  const weekNumOrderToWeekId = {};
  page_dict.value.forEach(item => {
      const key = `${item.week_num}_${item.order}`;
      weekNumOrderToWeekId[key] = item.week_id;
  });
  const regex4 = /\[(.*?)\]\s*\(\s*page\/(\d+)\/(\d+)\/(\d+)\s*\)/g;
  content = content.replace(regex4, (match, linkText, weekNum, order, page) => {
    const key = `${weekNum}_${order}`;
    const weekId = weekNumOrderToWeekId[key] || weekNum; // `week_id` がなければ `week_num` を使用
    console.log(`置換対象: ${match} → weekNum: ${weekNum}, order: ${order}, page: ${page}, 置換後のweekId: ${weekId}`);
    return `<div class='box'><p>[${linkText}](./../${weekId}/${page})</p></div>`;
  });
  return content
}

const reflection_content = () => {
  pr_content.value = content_replace(content.value)
  pr_content.value = markdownToHtml(pr_content.value)
  reloadMathJax()
}

// created
get_week_origin_content(1)

</script>

<template>
  <div>
    <v-tabs v-model='tab' fixed-tabs bg-color='grey-lighten-3' slider-color='secondary'>
      <v-tab v-for='p_content in origin_content' :value='p_content.page' class='bg-primary' @click='content = p_content.content; reflection_content()'>{{ p_content.page }}</v-tab>
    </v-tabs>
    <v-container>
      <v-tabs-window v-model='tab'>
        <v-tabs-window-item v-for='p_content in origin_content' :value='p_content.page'>
          <v-row class='justify-center my-3 mx-3'>
            <v-btn class='bg-secondary align-center mx-3' @click='reflection_content()'>反映</v-btn>
            <v-btn class='bg-secondary align-center mx-3' @click='update_week_content(content_id=p_content.content_id, origin_content_id=p_content.origin_content_id, page=p_content.page)'>更新</v-btn>
          </v-row>
          <v-row>
            <v-col cols='6'>
              <v-textarea rows='30' v-model='content'/>
            </v-col>
            <v-col cols='6'>
              <v-container class='mt-3' style="line-height: 2;">
                <MathJaxComp>
                  <div v-html='pr_content'/>
                </MathJaxComp>
              </v-container>
            </v-col>
          </v-row>
        </v-tabs-window-item>
      </v-tabs-window>
    </v-container>
  </div>
</template>

<style>
.indent_1 {
  padding-left: 20px;
}
.indent_2 {
  padding-left: 40px;
}
.solid_border_1 {
  padding: 10px;
  margin-bottom: 10px;
  border: 1px solid #333333;
}
.dashed_border_1 {
  padding: 10px;
  margin-bottom: 10px;
  border: 1px dashed #333333;
}
.example {
  padding: 10px;
  margin-bottom: 10px;
  border: 2px dashed #333333;
}
.answer {
  text-align: center;
  width:40px;
  margin: 1em;
  border: solid 2px #000000;
}
.definition {
  padding: 10px;
  margin-bottom: 10px;
  border: 2px solid #333333;
}
</style>
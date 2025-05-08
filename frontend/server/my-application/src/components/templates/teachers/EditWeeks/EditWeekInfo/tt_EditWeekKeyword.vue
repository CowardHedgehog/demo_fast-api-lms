<script setup>
import axios from 'axios'
import { ref, watch } from 'vue'

const type = ref('')

const keyword = ref([
  {name: '極限', url: 'https://manabitimes.jp/math/1040', comment:'数列の発散、収束などの内容'},
  {name: 'べき関数', url: 'https://manabitimes.jp/math/1115', comment:'それぞれの指数関数のグラフの概形'},
  {name: '指数関数', url: 'https://manabitimes.jp/math/1115', comment:'それぞれの指数関数のグラフの概形'},
  {name: '三角関数', url: 'https://manabitimes.jp/math/660', comment:'それぞれの指数関数のグラフの概形'},
  {name: '逆三角関数', url: 'https://manabitimes.jp/math/787', comment:'それぞれの指数関数のグラフの概形'},
  {name: '微分', url: 'https://univ-juken.com/bibun#i-4', comment:'三角・指数・対数・積・商・合成関数の微分・べき乗'},
  {name: '導関数', url: 'https://manabitimes.jp/math/1425', comment:''},
  {name: '対数関数', url: 'https://manabitimes.jp/math/2046', comment:'対数の定義、計算、微分'},
  {name: '有理関数', url: 'https://univ-juken.com/bunsu-kansu', comment:'サイト「受験辞典」（有理関数は分数関数ともいう）'},
  {name: '因数分解', url: 'https://univ-juken.com/innsu-bunkai', comment:'サイト「受験辞典」'},
  {name: '合成関数', url: 'https://manabitimes.jp/math/936', comment:'合成関数の微分法'},
  {name: '線形結合', url: 'https://www.krrk0.com/primary-independenceprimary-subordination/', comment:'サイト「『なんとなくわかる』大学の数学・物理・情報」１次従属・独立における１次結合を線形結合という'},
])

</script>

<template>
  <v-container class='bg-grey-lighten-2 rounded-lg'>
    <v-card>
      <v-card-title class='ma-4'><b><u>キーワードの編集</u></b></v-card-title>
      <v-card-text>
        <v-data-table :items='keyword' class='px-10'>
          <template v-slot:top>
            <v-toolbar-title>コンテンツ内に表示するキーワード</v-toolbar-title>
          </template>
          <template v-slot:item.url='{ item }'>
            <a :href='item.url' target='_blank'>{{ item.url }}</a>
          </template>
        </v-data-table>
      </v-card-text>
    </v-card>
  </v-container>
</template>
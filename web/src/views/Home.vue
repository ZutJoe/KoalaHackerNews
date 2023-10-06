<template>
  <el-table :data="tableData" border class="mx-auto w-70% text-center">
    <el-table-column 
        prop="time"
        label="时间轴" 
        >
        <template #default="scope">
            <el-link :href="scope.row.timeLink" target="_blank" type="primary">{{ scope.row.time }}</el-link>
        </template>
    </el-table-column>
    <el-table-column 
        prop="introduce" 
        label="简介" 
        />
    <el-table-column 
        prop="link" 
        label="链接" 
        />
  </el-table>
</template>


<script setup lang="ts">
// import axios from 'axios'
import { ref, onMounted } from 'vue'
import { TableType } from './type.ts'

const tableData = ref<TableType[]>([])

const data = [
  {
    "aid": 903386514,
    "hn_items": {
      "times": [
        {
          "minutes": 0,
          "seconds": 9
        },
        {
          "minutes": 0,
          "seconds": 39
        },
        {
          "minutes": 1,
          "seconds": 3
        },
        {
          "minutes": 1,
          "seconds": 28
        },
        {
          "minutes": 1,
          "seconds": 50
        },
        {
          "minutes": 2,
          "seconds": 9
        },
        {
          "minutes": 2,
          "seconds": 25
        }
      ],
      "introduces": [
        "OpenAI 开放 ChatGPT 模型",
        "Google 推出安全编程语言 Rune",
        "Kubeshark｜k8s 流量观测工具",
        "cheat.sh｜技术小抄集合",
        "go-coffeeshop｜GO 的微服务示例",
        "NLP 在线课程",
        "《Sql for Devs》｜数据库详解电子书"
      ],
      "links": [
        "https://openai.com/blog/chatgpt/",
        "https://github.com/google/rune",
        "https://github.com/kubeshark/kubeshark",
        "https://github.com/chubin/cheat.sh",
        "https://github.com/thangchung/go-coffeeshop",
        "https://www.nlpdemystified.org/",
        "https://sqlfordevs.com/ebook"
      ]
    }
  },
  {
    "aid": 690620840,
    "hn_items": {
      "times": [
        {
          "minutes": 0,
          "seconds": 9
        },
        {
          "minutes": 0,
          "seconds": 27
        },
        {
          "minutes": 0,
          "seconds": 51
        },
        {
          "minutes": 1,
          "seconds": 10
        },
        {
          "minutes": 1,
          "seconds": 39
        },
        {
          "minutes": 1,
          "seconds": 58
        },
        {
          "minutes": 2,
          "seconds": 20
        }
      ],
      "introduces": [
        "Script Kit｜面向开发者的自动化工具，",
        "D2｜开源声明式绘图语言",
        "Superset｜开源数据可视化平台",
        "Stable Diffusion 发布2.0版本",
        "蚂蚁 UI 组件库 Ant Design 发布 V5 版本",
        "《命令行的艺术》项目",
        "Diátaxis｜帮助创作技术文档的写作框架"
      ],
      "links": [
        "https://www.scriptkit.com/",
        "https://d2lang.com/",
        "https://superset.apache.org/",
        "https://stability.ai/blog/stable-diffusion-v2-release",
        "https://github.com/ant-design/ant-design/issues/38671",
        "https://github.com/jlevy/the-art-of-command-line",
        "https://diataxis.fr/"
      ]
    }
  }
]

onMounted(() => {
  data.map((item) => {
    for (let i = 0; i < item.hn_items.times.length; i++) {
        tableData.value.push({
            time: `${item.hn_items.times[i].minutes}:${item.hn_items.times[i].seconds}`,
            timeLink: `https://www.bilibili.com/video/av774867810?t=${item.hn_items.times[i].minutes * 60 + item.hn_items.times[i].seconds}`,
            introduce: item.hn_items.introduces[i],
            link: item.hn_items.links[i]
        })
    }
  })
  console.log(tableData.value);
  
})

onMounted(() => {

})

// axios.get('https://raw.githubusercontent.com/ZutJoe/Koala_hacker_news/dev/data.json')
// .then((response) => {
//   console.log(response.data)
// })


</script>

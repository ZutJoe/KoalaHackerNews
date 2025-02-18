<script setup lang="ts">
import { onMounted, ref } from 'vue';

import Card from 'primevue/card';
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';

type FormDataType = {
  aid: string,
  hn_items: {
    times: {
      minutes: number,
      seconds: number
    }[]
  },
  introduces: string[],
  links: string[]
}
const formData = ref<FormDataType[]>()
onMounted(async () => {
  console.log('mounted');
  const response = await fetch('https://raw.githubusercontent.com/ZutJoe/KoalaHackerNews/main/data.json')
  if (response.ok) {
    const data = await response.json()
    formData.value = data
    console.log(data)
  }
});
</script>

<template>
  <Card v-for="item in formData" :key="item.aid" class="customCard">
    <template #title>
      <a :href="'https://www.bilibili.com/video/av' + item.aid" :id="item.aid">视频链接</a>
    </template>
    <template #content>
      <DataTable>
        <Column header="Code"></Column>
      </DataTable>
    </template>
  </Card>
</template>

<style scoped>
.customCard {
  width: 70%;
  margin-top: 40px;
  margin-left: auto;
  margin-right: auto;
}

a {
  text-decoration: none;
}

</style>

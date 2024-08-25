<template>
  <div style="display: flex" class="codingEditor">
    <div ref="editorContainer" class="editorContainer"></div>
    <div class="btns">
      <button @click="saveCode">保存代码</button>
    </div>
  </div>
</template>

<style>
.codingEditor {
  width: 100%;
  height: 100%;
  border-radius: 10px;
}
.editorContainer {
  width: 80%;
  height: 100%;
}
.btns {
}
</style>
<script setup>
import { editor } from 'monaco-editor'
import { ref, onMounted } from 'vue'
import axios from 'axios'
const code = ref('')

const saveCode = () =>
  axios.post('http://127.0.0.1:8000/code/save/', {
    code: code.value
  })

const getCode = () => {
  axios.get('http://127.0.0.1:8000/code/').then((res) => {
    code.value = res.data.code
  })
}

const editorContainer = ref(null)
onMounted(() => {
  getCode()
  const codeEditor = editor.create(editorContainer.value, {
    value: code.value,
    language: 'python',
    minimap: {
      enabled: true
    },
    colorDecorators: true, //颜色装饰器
    readOnly: false, //是否开启已读功能
    theme: 'vs-dark', //主题,
    fontSize: 16,
    automaticLayout: true
  })
  // 监听编辑器内容变化
  codeEditor.onDidChangeModelContent(() => {
    // 触发父组件的 change 事件，通知编辑器内容变化
    code.value = codeEditor.getValue()
  })
})
</script>
